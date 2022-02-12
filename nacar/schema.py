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


class InvalidSchemaError(Exception):
    """
    The blueprint provided by the user did not contain a valid Nacar schema.
    """

    def __init__(self, validator_errors):
        errors_by_key = {}
        print(validator_errors)

        def walk_errors(errors_tree: dict, dotpath=""):
            # Traverse the validator errors object and stop at each error.
            for k, v in sorted(errors_tree.items(), key=lambda d: d[0]):
                dotpath = k if dotpath == "" else f"{dotpath}.{k}"
                if isinstance(v, dict):
                    walk_errors(v, dotpath)
                elif isinstance(v, list) and len(v) and isinstance(v[0], dict):
                    walk_errors(v[0], dotpath)
                else:
                    errors_by_key[dotpath] = v

        if len(validator_errors) > 0:
            walk_errors(validator_errors)

            print("\nPlease amend these schema errors in your blueprint:")
            pad_length = max(map(len, errors_by_key))
            key: str
            errors: list
            for key, errors in errors_by_key.items():
                key = f"{key}:".ljust(pad_length + 1)
                errors = [e for e in errors if isinstance(e, str)]
                print(f"{key} {', '.join(errors)}")
