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
        is_valid: bool = super(NacarValidator, self).validate(document, schema)
        return is_valid
