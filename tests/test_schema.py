# Nacar
# Copyright 2022 Alberto Morón Hernández
# [github.com/albertomh/Nacar]
#
# Test the Schema module
# ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
# Test adding subschemas to the registry, setting missing optional attributes,
# schema property getters, and raising custom InvalidSchemaErrors.


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
