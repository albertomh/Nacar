"""
Nacar
Copyright 2022 Alberto Morón Hernández
[github.com/albertomh/Nacar]

Custom Cerberus Validator
▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
TODO: document
"""

from typing import List

from cerberus import Validator

from schema import Schema


class NacarValidator(Validator):

    def validate(self, document, schema) -> bool:
        if document is None or schema is None:
            error_message = "The Nacar validator was not handed a "
            if document is None and schema is None:
                error_message += "schema or a document to validate."
            elif document is None and schema is not None:
                error_message += "document to validate."
            elif document is not None and schema is None:
                error_message += "schema to validate against."
            raise RuntimeError(error_message)

        # Validate with Cerberus.
        is_valid: bool = super(NacarValidator, self).validate(document, schema)

        # Check uniqueness of screen names.
        screen_names_are_unique = False
        screen_names: List[str] = Schema.get_screen_names(document)
        if len(screen_names) > 0:
            screen_names_are_unique = len(screen_names) == len(set(screen_names))  # noqa
            if not screen_names_are_unique:
                super(NacarValidator, self)._error('screens', "All screen names must be unique.")  # noqa

        return (is_valid and screen_names_are_unique)
