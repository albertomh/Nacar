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
from cerberus import Validator


class Schema:

    def __init__(self):
        self.validator = None
        self.add_blueprint_schema_to_validator()

    @staticmethod
    def get_blueprint_schema() -> dict:
        schema = {
            'title': {'type': 'string', 'required': True, 'minlength': 1, 'maxlength': 178},  # noqa

            'meta': {
                'type': 'dict',
                'required': False,
                'schema': {
                    'width': {'type': 'integer', 'required': False, 'min': 0, 'max': 180}  # noqa
                }
            },

            'screens': {
                'type': 'list',
                'required': True,
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'name': {'type': 'string', 'required': True, 'minlength': 1, 'maxlength': 64},      # noqa
                        'options': {
                            'type': 'list',
                            'minlength': 1,
                            'maxlength': 999,
                            'schema': {
                                'type': 'dict',
                                'anyof_schema': [
                                    {
                                        'name': {'type': 'string', 'required': True, 'minlength': 1, 'maxlength': 64},    # noqa
                                        'link': {'type': 'string', 'required': True, 'minlength': 1, 'maxlength': 64}     # noqa
                                    },
                                    {
                                        'name': {'type': 'string', 'required': True, 'minlength': 1, 'maxlength': 64},    # noqa
                                        'action': {'type': 'string', 'required': True, 'minlength': 1, 'maxlength': 256}  # noqa
                                    }
                                ]
                            }
                        }
                    }
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
