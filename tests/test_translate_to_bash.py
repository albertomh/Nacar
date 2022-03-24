# Nacar
# Copyright 2022 Alberto Morón Hernández
# [github.com/albertomh/Nacar]
#
# Test the to_bash Translator
# ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
# Test Translator initialisation, generation of dynamic snippets, and
# composition of resulting Nacar app string.


from os import path as os_path
from typing import Union, List
from json import loads as json_loads

import pytest

from nacar.translate.target_language import TargetLanguage
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


#   Test Translator initialisation ─────────────────────────────────────────────

def test_set_screens_was_called_upon_init(to_bash_translator):
    assert to_bash_translator.screens == ['home', 'develop', 'test']


#   Test Translator utilities ──────────────────────────────────────────────────

def test_get_target_language(to_bash_translator):
    assert to_bash_translator.get_target_language() == TargetLanguage.BASH


@pytest.mark.parametrize('content,lpad,expected', [
    ("", None,
     ["#"]),
    ("Test get_comment_lines() without specifying an lpad value.", None,
     ["# Test get_comment_lines() without specifying an lpad value."]),
    ("Test with lpad.", 8,
     ["        # Test with lpad."]),
    (["Test a multiline comment", "with three different lines", "without specifying lpad."], None,  # noqa
     ["# Test a multiline comment", "# with three different lines", "# without specifying lpad."]),  # noqa
    (["Test multiple comment", "lines with lpad."], 4,
     ["    # Test multiple comment", "    # lines with lpad."]),
    ("It is also necessary to test a really long single comment that exceeds the line limit of 80 characters.", None,  # noqa
     ["# It is also necessary to test a really long single comment that exceeds the", "# line limit of 80 characters."]),  # noqa,
    (["We must not neglect to test a comment spanning multiple lines with a really long line",  "as one of its elements."], None,  # noqa
     ["# We must not neglect to test a comment spanning multiple lines with a really long line", "# as one of its elements."]),  # noqa
    ("Here we test a comment that exceeds the eighty-character limit and which we would like indented.", 4,  # noqa
     ["    # Here we test a comment that exceeds the eighty-character limit and which we", "    # would like indented."]),  # noqa
])
def test_get_comment_lines(
        to_bash_translator: BlueprintToBash,
        content: Union[str, List[str]],
        lpad: Union[int, None],
        expected: List[str]
):
    result: List[str]
    if lpad is None:
        result = to_bash_translator.get_comment_lines(content)
    else:
        result = to_bash_translator.get_comment_lines(content, lpad)

    assert result == expected


@pytest.mark.parametrize('title,rule_char,expected', [
    ("This is a section title", None, "# ───── This is a section title ────────────────────────────────────────────────"),  # noqa
    ("This is another section title", '*', "# ***** This is another section title ******************************************"),  # noqa
    ("This is a section title that really gets out of hand, really it is longer than it has any right to be", None, "# ───── This is a section title that really gets out of hand, really it is longer than it has any right to be"),  # noqa
])
def test_get_section_title(
        to_bash_translator: BlueprintToBash,
        title: str, rule_char: Union[str, None], expected: str
):
    result: str
    if rule_char is None:
        result = to_bash_translator.get_section_title(title)
    else:
        result = to_bash_translator.get_section_title(title, rule_char)

    assert result == expected
