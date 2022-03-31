"""
Nacar
Copyright 2022 Alberto Morón Hernández
[github.com/albertomh/Nacar]

Schema utilities
▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
Create modular subschemas to add to the Cerberus schema registry,
set missing optional attributes on a blueprint, get properties
from the parsed blueprint.
"""

from typing import List, Dict

from cerberus import schema_registry


class Schema:

    def __init__(self):
        self.add_blueprint_subschemas_to_registry()

    @staticmethod
    def get_blueprint_subschemas() -> dict:
        modular_schemas = {
            'meta': {
                'authors': {
                    'type': 'list', 'minlength': 1, 'maxlength': 10,
                    'schema': {'type': 'string', 'required': False, 'minlength': 1, 'maxlength': 64}  # noqa
                },
                'width': {'type': 'integer', 'required': False, 'min': 40, 'max': 180},               # noqa
                'show_made_with_on_exit': {'type': 'boolean', 'required': False}
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

    @staticmethod
    def add_blueprint_subschemas_to_registry():
        """
        Add modular blueprint schemas to Cerberus' default schema registry.
        """
        for name, schema in Schema.get_blueprint_subschemas().items():
            schema_registry.add(name, schema)

    @staticmethod
    def get_blueprint_schema() -> dict:
        return {
            'title': {'type': 'string', 'required': True, 'minlength': 1, 'maxlength': 178},  # noqa

            'meta': {
                'type': 'dict',
                'required': False,
                'schema': 'meta'
            },

            'screens': {
                'type': 'list',
                'required': True,
                'minlength': 1,
                'maxlength': 999,
                'schema': {
                    'type': 'dict',
                    'schema': 'screen'
                }
            }
        }

    @staticmethod
    def set_missing_optional_attributes(blueprint: dict) -> dict:
        def exists(obj: dict, chain: List[str]) -> bool:
            _key = chain.pop(0)
            if _key in obj:
                if len(chain) > 0:
                    return exists(obj[_key], chain)
                else:
                    return obj[_key] is not None
            return False

        if not exists(blueprint, ['meta', 'width']):
            blueprint['meta']['width'] = 80
        if not exists(blueprint, ['meta', 'show_made_with_on_exit']):
            blueprint['meta']['show_made_with_on_exit'] = True

        return blueprint

    @staticmethod
    def get_screen_names(blueprint: dict) -> List[str]:
        """
        Return a flat list of every screen name in the blueprint.
        """
        if len(blueprint) > 0 and 'screens' in blueprint:
            return [s['name'] for s in blueprint['screens']]

        return []

    @staticmethod
    def get_screen_links(blueprint: dict) -> List[List[str]]:
        """
        Return a list of [screen1, screen2] pairs showing
        how screens link to other screens.
        """
        if len(blueprint) > 0 and 'screens' in blueprint:
            return [[s['name'], o['link']]
                    for s in blueprint['screens'] if 'options' in s
                    for o in s['options'] if 'link' in o]

        return []

    @staticmethod
    def get_max_screen_options_in_blueprint(blueprint: dict) -> int:
        """
        @param blueprint {dict}: the blueprint under consideration.
        @return {int}: the number of options in the screen with most options.
        """
        number_of_options_per_screen: List[int] = []
        for screen in Schema.get_screen_names(blueprint):
            options_count = len(Schema.get_options_for_screen(blueprint, screen))  # noqa
            number_of_options_per_screen += [options_count]

        return max(number_of_options_per_screen)

    @staticmethod
    def get_options_for_screen(blueprint: dict, screen_name: str) -> list:
        for screen in blueprint['screens']:
            if screen['name'] == screen_name:
                return screen['options']


class InvalidSchemaError(Exception):
    """
    The blueprint provided by the user did not contain a valid Nacar schema.
    """
    _error_lines: List[str]

    def __init__(self, validator_errors: dict):
        self._error_lines = []
        _errors_by_key: Dict[str, List[str]] = {}

        # validator_errors has the following shape:
        # { 'schema_key': [{
        #     'subkey1': [ "err1-1", ... ],
        #     'subkey2': [ "err2-1", ... ] }]
        # }
        def walk_errors(validator_errors: dict, breadcrumbs: List[str]=None):
            if breadcrumbs is None:
                breadcrumbs = []
            keys = validator_errors.keys()
            level_keys = list(keys)
            for key in keys:
                errors = validator_errors[key]
                breadcrumbs.append(key)
                level_keys = [k for k in level_keys if k != key]

                if isinstance(errors[0], dict) and len(errors[0].keys()) > 0:
                    walk_errors(errors[0], breadcrumbs)

                # Important! Manipulating `breadcrumbs` below with `pop()` has
                # been carefully chosen so that the same object is always kept
                # in memory. Assigning `= []` in order to empty or slicing [:-1]
                # create new lists, leading to a subtle, tricky bug.
                elif isinstance(errors[0], str):
                    errors = [err.capitalize() + ('.' if err[-1] != '.' else '')
                              for err in errors if isinstance(err, str)]
                    breadcrumbs_key = '.'.join([b for b in breadcrumbs
                                                if isinstance(b, str)])
                    _errors_by_key[breadcrumbs_key] = errors
                    if len(level_keys) > 0:
                        breadcrumbs.pop()
                    else:
                        while len(breadcrumbs):
                            breadcrumbs.pop()

        if len(validator_errors) > 0:
            walk_errors(validator_errors)

            self._error_lines.append("Please amend these schema errors in your blueprint:")  # noqa
            pad_length = max(map(len, _errors_by_key))
            key: str
            errors: list
            for key, errors in _errors_by_key.items():
                key = f"{key}:".ljust(pad_length + 1)
                for e in [e for e in errors if isinstance(e, str)]:
                    self._error_lines.append(f"{key} {e}".replace('.,', ','))

    @property
    def message(self) -> str:
        return '\n'.join(self._error_lines)
