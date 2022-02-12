#!/usr/bin/env python3

"""
Nacar
Copyright 2022 Alberto Morón Hernández
[github.com/albertomh/Nacar]

Schema utilities
▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
TODO: document
"""

from yaml.scanner import ScannerError
from cerberus import schema_registry
from cerberus import Validator


class Schema:

    def __init__(self):
        self.validator = None
        self.add_blueprint_subschemas_to_registry()
        self.add_blueprint_schema_to_validator()

    @staticmethod
    def get_blueprint_subschemas() -> dict:
        modular_schemas = {
            'meta': {
                'authors': {
                    'type': 'list', 'minlength': 1, 'maxlength': 10,
                    'schema': {'type': 'string', 'required': False, 'minlength': 1, 'maxlength': 64}  # noqa
                },
                'width': {'type': 'integer', 'required': False, 'min': 0, 'max': 180}                 # noqa
            },

            'screen': {
                'name': {'type': 'string', 'required': True, 'minlength': 1, 'maxlength': 64},        # noqa
                'options': {
                    'type': 'list',
                    'minlength': 1,
                    'maxlength': 999,
                    'schema': {
                        'type': 'dict',
                        'anyof_schema': ['screen__option--link', 'screen__option--action']            # noqa
                    }
                }
            },
            'screen__option--link': {
                'name': {'type': 'string', 'required': True, 'minlength': 1, 'maxlength': 64},        # noqa
                'link': {'type': 'string', 'required': True, 'minlength': 1, 'maxlength': 64}         # noqa
            },
            'screen__option--action': {
                'name': {'type': 'string', 'required': True, 'minlength': 1, 'maxlength': 64},        # noqa
                'action': {'type': 'string', 'required': True, 'minlength': 1, 'maxlength': 256}      # noqa
            }
        }

        return modular_schemas

    def add_blueprint_subschemas_to_registry(self):
        """
        Add modular blueprint schemas to Cerberus' default schema registry.
        """
        for name, schema in Schema.get_blueprint_subschemas().items():
            schema_registry.add(name, schema)

    @staticmethod
    def get_blueprint_schema() -> dict:
        schema = {
            'title': {'type': 'string', 'required': True, 'minlength': 1, 'maxlength': 178},  # noqa

            'meta': {
                'type': 'dict',
                'required': False,
                'schema': 'meta'
            },

            'screens': {
                'type': 'list',
                'required': True,
                'schema': {
                    'type': 'dict',
                    'schema': 'screen'
                }
            }
        }

        return schema

    def add_blueprint_schema_to_validator(self):
        """
        Pass the main blueprint schema to the Cerberus validator.
        """
        try:
            blueprint_schema: dict = Schema.get_blueprint_schema()
        except (FileNotFoundError, ScannerError) as e:
            print(str(e))
            return
        self.validator = Validator(blueprint_schema)

    def get_validator(self):
        return self.validator
