# Nacar
# Copyright 2022 Alberto Morón Hernández
# [github.com/albertomh/Nacar]
#
# Test the to_bash Translator
# ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
# Test Translator initialisation, generation of dynamic snippets, and
# composition of resulting Nacar app string.


from os import path as os_path
from json import loads as json_loads

import pytest

from nacar.translate.to_bash.to_bash import BlueprintToBash


# scope='module' ensures this is instantiated only once per test module
# rather than once per test method as is default.
@pytest.fixture(scope='module', autouse=True)
def to_bash_translator(test_data_dir) -> BlueprintToBash:
    valid_output_json_path = os_path.join(test_data_dir, 'valid-blueprint.json')
    blueprint: dict
    with open(valid_output_json_path) as file:
        blueprint = json_loads(file.read())
        # Set optional parameters to emulate `Schema.set_missing_optional_attributes()`.  # noqa
        blueprint['meta']['show_made_with_on_exit'] = True

    return BlueprintToBash(blueprint)
