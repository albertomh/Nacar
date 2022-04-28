# Nacar
# Copyright 2022 Alberto Morón Hernández
# [github.com/albertomh/Nacar]
#
# Test the Validator module
# ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
# Test the Validator extends Cerberus correctly, and that custom schemas
# are correctly validated when an invalid document is supplied.

from os import path as os_path
from json import loads as json_loads

import pytest

from nacar.schema import Schema
from nacar.validator import NacarValidator


#   Test `validate()` ──────────────────────────────────────────────────────────

# scope='module' ensures this is instantiated only once per test module
# rather than once per test method as is default.
@pytest.fixture(scope='module', autouse=True)
def nacar_schema() -> None:
    """
    Must instantiate a Schema object before every test since
    blueprint subschemas are added to the Cerberus registry
    as part of the Schema object's initialisation.
    """
    Schema()


@pytest.fixture
def nacar_validator() -> NacarValidator:
    return NacarValidator()


@pytest.fixture
def blueprint_schema() -> dict:
    return Schema.get_blueprint_schema()


@pytest.mark.parametrize('document,schema,error_msg', [
    (None, None, "The Nacar validator was not handed a schema or a document to validate."),  # noqa
    (None, {}, "The Nacar validator was not handed a document to validate."),
    ({}, None, "The Nacar validator was not handed a schema to validate against.")  # noqa
])
def test_validate_with_missing_params(
    nacar_validator: NacarValidator,
    document: dict,
    schema: dict,
    error_msg: str
) -> None:
    with pytest.raises(RuntimeError, match=error_msg):
        nacar_validator.validate(document, schema)


# `invalid_blueprint_filename` points to a JSON file in `/tests/data/`.
@pytest.mark.parametrize('invalid_blueprint_filename', [
    'invalid-blueprint--missing-title.json',
    'invalid-blueprint--empty-screens.json'
])
def test_cerberus_validation(
    blueprint_schema: dict,
    nacar_validator: NacarValidator,
    test_data_dir: str,
    invalid_blueprint_filename: str
):
    """
    Test the call in NacarValidator::validate to Cerberus' validate() method.
    """
    with open(os_path.join(test_data_dir, invalid_blueprint_filename)) as file:
        invalid_blueprint: dict = json_loads(file.read())
        assert nacar_validator.validate(invalid_blueprint, blueprint_schema) is False  # noqa


@pytest.mark.parametrize('invalid_blueprint,expected_errors', [
    # Reject non-unique screen names.
    ({'screens': [{'name': 'home'}, {'name': 'home'}]},
     {'screens': ['All screen names must be unique.'], 'title': ['required field']}),  # noqa
    # Ensure screens do not link to themselves.
    ({'screens': [{'name': 'home', 'options': [{'name': 'Self-link', 'link': 'home'}]}]},  # noqa
     {'screens': ['Screens must not link to themselves.'], 'title': ['required field']}),  # noqa
    # Ensure all links point to existing screens.
    ({'screens': [{'name': 'home', 'options': [{'name': 'Inexistent link', 'link': 'inexistentScreen'}]}]},  # noqa
     {'screens': ['Cannot link to an undefined screen.'], 'title': ['required field']}),  # noqa
])
def test_validator_rejects_non_unique_screen_names(
    blueprint_schema: dict,
    nacar_validator: NacarValidator,
    invalid_blueprint: dict,
    expected_errors: dict
) -> None:
    is_valid = nacar_validator.validate(invalid_blueprint, blueprint_schema)
    cerberus_errors = super(NacarValidator, nacar_validator).errors
    assert cerberus_errors == expected_errors
    assert is_valid is False
