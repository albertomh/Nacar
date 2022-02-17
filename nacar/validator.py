"""
Nacar
Copyright 2022 Alberto Morón Hernández
[github.com/albertomh/Nacar]

Custom Cerberus Validator
▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
TODO: document
"""

from cerberus import Validator


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

        return is_valid
