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

from nacar.schema import Schema
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
                'options': [{'name': 'Develop', 'link': 'develop'}, {'name': 'Test', 'link': 'test'}]
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
    # TODO: add other optional attributes as they are added in `set_missing_optional_attributes()`.
])
def test_set_missing_optional_attributes__meta_width(
    blueprint: dict,
    path_chain: list,
    default_value
) -> None:
    assert get_nested_key(blueprint, path_chain) is None
    blueprint = Schema.set_missing_optional_attributes(blueprint)
    assert get_nested_key(blueprint, path_chain) == default_value

