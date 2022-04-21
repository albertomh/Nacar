# Nacar
# Copyright 2022 Alberto Morón Hernández
# [github.com/albertomh/Nacar]
#
# Test the Schema module
# ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
# Test adding subschemas to the registry, setting missing optional attributes,
# schema property getters, and raising custom InvalidSchemaErrors.

import pytest
from cerberus import schema_registry

from nacar.schema import Schema, InvalidSchemaError
from tests.utils import get_nested_key


@pytest.fixture()
def blueprint() -> dict:
    return {
        'title': 'Test Blueprint',
        'meta': {
            'authors': [
                'Author Lastname'
            ]
        },
        'screens': [
            {
                'name': 'home',
                'options': [{'name': 'Develop', 'link': 'develop'}, {'name': 'Test', 'link': 'test'}]  # noqa
            },
            {
                'name': 'develop',
                'options': [{'name': 'build', 'action': "echo 'build code'"}]
            },
            {
                'name': 'test',
                'options': [{'name': 'run', 'action': "echo 'run tests'"}]
            }
        ]
    }


def cerberus_registry_contains_expected_subschemas(registry) -> bool:
    schemas_in_registry_count = len(registry.all().keys())

    expected_subschema_names = sorted([
        'meta',
        'screen',
        'screen__option--link',
        'screen__option--action'
    ])
    actual_subschema_keys = sorted(registry.all().keys())

    return (schemas_in_registry_count == len(expected_subschema_names)
            and (expected_subschema_names == actual_subschema_keys))


def test_instantiating_schema_adds_subschemas_to_cerberus() -> None:
    schema_registry.clear()
    Schema()
    assert cerberus_registry_contains_expected_subschemas(schema_registry) is True  # noqa


def test_add_blueprint_subschemas_to_registry():
    schema_registry.clear()
    Schema.add_blueprint_subschemas_to_registry()
    assert cerberus_registry_contains_expected_subschemas(schema_registry) is True  # noqa


@pytest.mark.parametrize('path_chain,default_value', [
    (['meta', 'width'], 80),
    (['meta', 'show_made_with_on_exit'], True),
])
def test_set_missing_optional_attributes__meta_width(
    blueprint: dict,
    path_chain: list,
    default_value
) -> None:
    assert get_nested_key(blueprint, path_chain) is None
    blueprint = Schema.set_missing_optional_attributes(blueprint)
    assert get_nested_key(blueprint, path_chain) == default_value


def test_get_screen_names(blueprint: dict):
    screen_names = Schema.get_screen_names(blueprint)
    expected_screen_names = ['home', 'develop', 'test']
    assert screen_names == expected_screen_names


def test_get_screen_links(blueprint: dict):
    screen_links = Schema.get_screen_links(blueprint)
    expected_screen_links = [['home', 'develop'], ['home', 'test']]
    assert screen_links == expected_screen_links


def test_get_max_screen_options_in_blueprint(blueprint: dict):
    expected_max_screen_options = 2
    max_screen_options = Schema.get_max_screen_options_in_blueprint(blueprint)  # noqa
    assert max_screen_options == expected_max_screen_options


@pytest.mark.parametrize('screen_name,expected_options', [
    ('home', [{'name': 'Develop', 'link': 'develop'}, {'name': 'Test', 'link': 'test'}]),    # noqa
    ('develop', [{'name': 'build', 'action': "echo 'build code'"}]),
    ('test', [{'name': 'run', 'action': "echo 'run tests'"}]),
])
def test_get_options_for_screen(
    blueprint: dict,
    screen_name: str,
    expected_options: list
) -> None:
    options_for_screen = Schema.get_options_for_screen(blueprint, screen_name)  # noqa
    assert options_for_screen == expected_options


@pytest.mark.parametrize('validator_errors,err_message', [
    ({'meta': [{'width': ['min value is 40']}]},
     "Please amend these schema errors in your blueprint:\nmeta.width: Min value is 40."),  # noqa
    ({'meta': [{'show_made_with_on_exit': ['must be of boolean type']}], 'screens': ['Screens must not link to themselves.']},  # noqa
     "Please amend these schema errors in your blueprint:\nmeta.show_made_with_on_exit: Must be of boolean type.\nscreens:                     Screens must not link to themselves."),  # noqa
])
def test_invalid_schema_error(validator_errors: dict, err_message: str):
    with pytest.raises(InvalidSchemaError) as excinfo:
        raise InvalidSchemaError(validator_errors)

    err: InvalidSchemaError = excinfo.value
    assert err.message == err_message
