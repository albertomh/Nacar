# Nacar
# Copyright 2022 Alberto Morón Hernández
# [github.com/albertomh/Nacar]
#
# Test the Validator module
# ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
# Test the Validator extends Cerberus correctly, and that custom schemas
# are correctly validated when an invalid document is supplied.

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
