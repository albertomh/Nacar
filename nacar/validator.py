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

        # Check screens do not link to themselves.
        screen_links: List[List[str]] = Schema.get_screen_links(document)
        screen_link_lengths: List[int] = [len(set(sl)) for sl in screen_links]
        # Each pair of screen links must contain two separate screen names.
        # If 1 is present, at least one recursive screen link of
        # the form [screen1, screen1] was found.
        screen_links_are_recursive = 1 in screen_link_lengths
        if screen_links_are_recursive:
            super(NacarValidator, self)._error('screens', "Screens must not link to themselves.")  # noqa

        return (is_valid
                and screen_names_are_unique
                and not screen_links_are_recursive)
