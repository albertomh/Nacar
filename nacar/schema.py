"""
Nacar
Copyright 2022 Alberto Morón Hernández
[github.com/albertomh/Nacar]

Schema utilities
▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
TODO: document
"""

from typing import List

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
                'width': {'type': 'integer', 'required': False, 'min': 40, 'max': 180}                # noqa
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
                'minlength': 1,
                'maxlength': 999,
                'schema': {
                    'type': 'dict',
                    'schema': 'screen'
                }
            }
        }

        return schema

    @staticmethod
    def set_missing_optional_attributes(blueprint: dict) -> dict:
        def exists(obj: dict, chain: list):
            _key = chain.pop(0)
            if _key in obj:
                return exists(obj[_key], chain) if chain else obj[_key]

        if not exists(blueprint, ['meta', 'width']):
            blueprint['meta']['width'] = 80

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

    def __init__(self, validator_errors):
        errors_by_key = {}

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
                for e in [e for e in errors if isinstance(e, str)]:
                    print(f"{key} {e}".replace('.,', ','))
