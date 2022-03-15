# Nacar
# Copyright 2022 Alberto Morón Hernández
# [github.com/albertomh/Nacar]
#
# Test the FileIO module
# ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
# Test persing YAML files, changing file mode, and writing Nacar apps to a file.

import os
from json import loads as json_loads

import pytest
from yaml.scanner import ScannerError

from nacar.file_io import FileIO


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
