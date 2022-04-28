# Nacar
# Copyright 2022 Alberto Morón Hernández
# [github.com/albertomh/Nacar]
#
# Test the to_bash Translator
# ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
# Test Translator initialisation, generation of dynamic snippets, and
# composition of resulting Nacar app string.


from os import path as os_path
from os.path import dirname, abspath
from json import loads as json_loads
import datetime
import hashlib

from unittest.mock import patch
import pytest
from jinja2 import Environment as JinjaEnvironment
from jinja2.loaders import FileSystemLoader as JinjaFSLoader

from nacar.translate.target_language import TargetLanguage
from nacar.translate.to_bash.to_bash import BlueprintToBash


# scope='module' ensures this is instantiated only once per test module
# rather than once per test method as is default.
@pytest.fixture(scope='module', autouse=True)
def to_bash_translator(test_data_dir) -> BlueprintToBash:
    valid_output_json_path = os_path.join(test_data_dir, 'valid-blueprint.json')  # noqa
    blueprint: dict
    with open(valid_output_json_path) as file:
        blueprint = json_loads(file.read())
        # Set optional parameters to emulate `Schema.set_missing_optional_attributes()`.  # noqa
        blueprint['meta']['show_made_with_on_exit'] = True

    return BlueprintToBash(blueprint)


#   Test Translator initialisation ─────────────────────────────────────────────

def test_set_screens_was_called_on_init(to_bash_translator):
    assert to_bash_translator.screens == ['home', 'develop', 'test']


def test_jinja_environment_was_set_on_init(to_bash_translator):
    env = to_bash_translator.jinja_env
    assert isinstance(env, JinjaEnvironment)
    assert isinstance(env.loader, JinjaFSLoader)

    nacar_root = dirname(dirname(abspath(__file__)))
    searchpath = env.loader.searchpath[0]
    expected_path = os_path.join(nacar_root, 'nacar', 'translate', 'to_bash', 'templates')  # noqa
    assert searchpath == expected_path

    assert env.trim_blocks is True
    assert env.lstrip_blocks is True


def test_template_data_is_empty_on_init(to_bash_translator):
    assert to_bash_translator.template_data == {}


#   Test Translator utilities ──────────────────────────────────────────────────

def test_get_target_language(to_bash_translator):
    assert to_bash_translator.get_target_language() == TargetLanguage.BASH


#   Test file heading utilities ────────────────────────────────────────────────

def get_expected_heading_template_data() -> dict:
    return {
        'title': 'Global Title',
        'current_year': 2022,
        'authors': 'Author',
        'nacar_version': '1.2.3',
        'current_date': '2022-01-01'
    }


def test_set_heading_template_variables(to_bash_translator):
    with patch('nacar.translate.to_bash.to_bash.datetime', wraps=datetime.datetime) as dt, \
            patch('nacar.translate.to_bash.to_bash.__version__', '1.2.3'):
        dt.now.return_value = datetime.datetime(2022, 1, 1)
        to_bash_translator.set_heading_template_variables()
        result = to_bash_translator.template_data

    expected = {
        'heading': get_expected_heading_template_data()
    }
    assert result == expected


#   Test Nacar app config ──────────────────────────────────────────────────────

def get_expected_app_config_template_variables() -> dict:
    return {
        'screen_width': 80
    }


def test_set_app_config_template_variables(to_bash_translator):
    to_bash_translator.set_app_config_template_variables()
    result = to_bash_translator.template_data

    expected = {
        'heading': get_expected_heading_template_data(),
        'app_config': get_expected_app_config_template_variables()
    }
    assert result == expected


#   Test utilities; Test screen-building utilities ─────────────────────────────

# Tests for these utilities intentionally not implemented since there is very
# little dynamic behaviour as most simply return static strings.


#   Test screen flow utilities ─────────────────────────────────────────────────

def get_expected_screen_flow_template_variables() -> dict:
    return {
        'screens': ['home', 'develop', 'test'],
        'screen_options': {
            'home': [{'link': 'develop', 'name': 'Develop'}, {'link': 'test', 'name': 'Test'}],
            'develop': [{'action': "echo 'build code'", 'name': 'build'}],
            'test': [{'action': "echo 'run tests'", 'name': 'run'}]
        }
    }


def test_set_screen_flow_template_variables(to_bash_translator):
    to_bash_translator.set_screen_flow_template_variables()
    result = to_bash_translator.template_data

    expected = {
        'heading': get_expected_heading_template_data(),
        'app_config': get_expected_app_config_template_variables(),
        'screen_flow': get_expected_screen_flow_template_variables()
    }
    assert result == expected


#   Test screen rendering utilities ────────────────────────────────────────────

def get_expected_screen_rendering_template_variables() -> dict:
    return {
        'show_made_with_on_exit': True,
        'bottom_padding_screen_map': {'develop': 2, 'home': 1, 'test': 2}
    }


def test_set_screen_rendering_template_variables(to_bash_translator):
    to_bash_translator.set_screen_rendering_template_variables()
    result = to_bash_translator.template_data

    expected = {
        'heading': get_expected_heading_template_data(),
        'app_config': get_expected_app_config_template_variables(),
        'screen_flow': get_expected_screen_flow_template_variables(),
        'screen_rendering': get_expected_screen_rendering_template_variables()
    }
    assert result == expected


#   Test main loop writer ──────────────────────────────────────────────────────

# Tests for these methods intentionally not implemented since dynamic behaviour
# that feeds through to these functions is defined in methods tested above.


#   Test translating blueprint to Bash ─────────────────────────────────────────

def test_translate_blueprint(to_bash_translator):
    translation = to_bash_translator.translate_blueprint()
    translation_hash = hashlib.md5(translation.encode('utf-8')).hexdigest()
    expected_hash = '934d970f9192bf9326c239163a7e5b84'
    assert translation_hash == expected_hash
