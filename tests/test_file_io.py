# Nacar
# Copyright 2022 Alberto Morón Hernández
# [github.com/albertomh/Nacar]
#
# Test the FileIO module
# ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
# Test persing YAML files, changing file mode, and writing Nacar apps to a file.

import os
import subprocess
import stat
from enum import Enum
from json import loads as json_loads

import pytest
from yaml.scanner import ScannerError

from nacar.file_io import FileIO
from nacar.translate.target_language import TargetLanguage


#   Test `parse_yml_file()` ───────────────────────────────────────────────────

def test_parsing_inexistent_file():
    path_to_inexistent_file = '/tmp/inexistent-blueprint.yml'
    error_msg = f"The specified file '{path_to_inexistent_file}' does not exist."  # noqa

    with pytest.raises(FileNotFoundError, match=error_msg):
        FileIO.parse_yml_file(path_to_inexistent_file)


def test_parsing_invalid_yaml_in_existing_file(test_data_dir):
    path_to_invalid_yaml = os.path.join(test_data_dir, 'invalid-yaml.yml')  # noqa
    error_msg = f"Invalid YAML in '{os.path.abspath(path_to_invalid_yaml)}'. Please provide a blueprint that is valid YAML."  # noqa

    with pytest.raises(ScannerError, match=error_msg):
        FileIO.parse_yml_file(path_to_invalid_yaml)


def test_parsing_valid_yaml_in_existing_file(test_data_dir):
    path_to_valid_yaml = os.path.join(test_data_dir, 'valid-blueprint.yml')  # noqa
    valid_output_json_path = os.path.join(test_data_dir, 'valid-blueprint.json')  # noqa

    blueprint = FileIO.parse_yml_file(path_to_valid_yaml)
    assert type(blueprint) is dict

    with open(valid_output_json_path) as file:
        valid_blueprint: dict = json_loads(file.read())
        assert blueprint == valid_blueprint


#   Test `make_file_executable()` ──────────────────────────────────────────────

def test_cannot_make_inexistent_file_executable():
    path_to_inexistent_file = '/tmp/nacar_test-inexistent-file'
    error_msg = f"Could not find '{os.path.abspath(path_to_inexistent_file)}' when attempting to make this file executable."  # noqa

    with pytest.raises(FileNotFoundError, match=error_msg):
        FileIO.make_file_executable(path_to_inexistent_file)


def file_is_executable_by_everyone(file_path) -> bool:
    mode = os.stat(file_path).st_mode
    return (bool(mode & stat.S_IXUSR)
            and bool(mode & stat.S_IXGRP)
            and bool(mode & stat.S_IXOTH))


def test_make_file_executable():
    tmp_file_path = os.path.join('/tmp', 'nacar_test-make-file-executable.sh')
    if os.path.exists(tmp_file_path):
        os.remove(tmp_file_path)

    with open(tmp_file_path, 'w') as tmp_file:
        tmp_file.write("echo 'Nacar executable test'")
    assert file_is_executable_by_everyone(tmp_file_path) is False

    FileIO.make_file_executable(tmp_file_path)
    assert file_is_executable_by_everyone(tmp_file_path) is True


#   Test `write_nacar_app_to_file()` ───────────────────────────────────────────

@pytest.fixture
def nacar_app_as_string():
    app_lines = [
        '#!/bin/bash',
        'repeat() {',
        '	  for i in $(seq 1 $2); do printf "$1"; done',
        '}',
        'repeat - 42'
    ]
    return '\n'.join(app_lines)


def test_writing_app_in_unimplemented_target_language(nacar_app_as_string):
    languages = [lang.name for lang in TargetLanguage] + ['COBOL']
    UnimplementedTargetLanguage = Enum('TargetLanguage', languages)

    error_msg = f"There is no writer configured for writing Nacar apps in " \
                f"{UnimplementedTargetLanguage.COBOL.name.title()}."
    with pytest.raises(NotImplementedError, match=error_msg):
        FileIO.write_nacar_app_to_file(
            nacar_app_as_string,
            os.path.join('/tmp', 'nacar_cobol-app'),
            UnimplementedTargetLanguage.COBOL
        )
