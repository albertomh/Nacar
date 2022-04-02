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
        'screen_width': 80,
        'title': 'Global Title'
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

def test_get_screen_flow_constants_lines(to_bash_translator: BlueprintToBash):
    expected = [
        'readonly HOME_SCREEN="home"',
        'readonly DEVELOP_SCREEN="develop"',
        'readonly TEST_SCREEN="test"'
    ]
    assert to_bash_translator.get_screen_flow_constants_lines() == expected


def test_get_check_keystroke_method_lines(to_bash_translator: BlueprintToBash):
    expected = [
        '# @param $1 The screen this function is invoked from.',
        '#           One of the _SCREEN constants declared above.',
        'check_keystroke() {',
        '    local prompt=" ${GRN}\\$${END}"',
        '    read -rs -p " ${prompt} " -n1 key',
        '',
        '    # Keypresses related to a screen.',
        '    if [[ "$1" == "$HOME_SCREEN" ]]; then',
        '        case "$key" in',
        '            "D" | "d")',
        '                navigate_to $DEVELOP_SCREEN; return 0;;',
        '            "T" | "t")',
        '                navigate_to $TEST_SCREEN; return 0;;',
        '        esac',
        '',
        '    elif [[ "$1" == "$DEVELOP_SCREEN" ]]; then',
        '        case "$key" in',
        '            "B" | "b")',
        '                INVOKE_ON_EXIT="echo \'build code\'"; return 1;;',
        '        esac',
        '',
        '    elif [[ "$1" == "$TEST_SCREEN" ]]; then',
        '        case "$key" in',
        '            "R" | "r")',
        '                INVOKE_ON_EXIT="echo \'run tests\'"; return 1;;',
        '        esac',
        '',
        '    fi',
        '',
        '    # Handle [ESC] key and left arrow.',
        '    # [unix.stackexchange.com/a/179193]',
        '    case "$key" in',
        "        $'\\x1b')  # Handle ESC sequence.",
        '            read -rsn1 -t 0.1 additional_bytes',
        '            if [[ "$additional_bytes" == "[" ]]; then',
        '                read -rsn1 -t 0.1 additional_bytes',
        '                case "$additional_bytes" in',
        '                    "D")  # Left arrow.',
        '                        navigate_back; return 0;;',
        '                    *)  # Other escape sequences.',
        '                        return 0;;',
        '                esac',
        '            fi;;',
        '        *)  # Other single byte (char) cases.',
        '            return 0;;',
        '    esac',
        '',
        '    # Default fallthrough.',
        '    return 1',
        '}'
    ]
    assert to_bash_translator.get_check_keystroke_method_lines() == expected


#   Test screen rendering utilities ────────────────────────────────────────────

def test_get_show_screen_methods_lines(to_bash_translator: BlueprintToBash):
    expected = [
        'show_home_screen() {',
        '    print_screen_top',
        '    printf "\\U2502 [${YEL}D${END}]evelop %66s \\U2502\\n"',
        '    printf "\\U2502 [${YEL}T${END}]est %69s \\U2502\\n"',
        '    print_screen_bottom 1', '',
        '    check_keystroke $HOME_SCREEN', '}',
        'show_develop_screen() {',
        '    print_screen_top',
        '    printf "\\U2502 [${YEL}B${END}]uild %68s \\U2502\\n"',
        '    print_screen_bottom 2', '',
        '    check_keystroke $DEVELOP_SCREEN', '}',
        'show_test_screen() {',
        '    print_screen_top',
        '    printf "\\U2502 [${YEL}R${END}]un %70s \\U2502\\n"',
        '    print_screen_bottom 2',
        '',
        '    check_keystroke $TEST_SCREEN', '}'
    ]
    assert to_bash_translator.get_show_screen_methods_lines() == expected


def test_get_show_exit_screen_lines(to_bash_translator: BlueprintToBash):
    expected = [
        'show_exit_screen() {',
        '    clear_screen',
        '    printf "Exited \\U1F41A Made with Nacar \\n\\n"',
        '}'
    ]
    assert to_bash_translator.get_show_exit_screen_lines() == expected


#   Test main loop writer; Test translating blueprint to Bash ──────────────────

# Tests for these methods intentionally not implemented since dynamic behaviour
# that feeds through to these functions is defined in methods tested above.
