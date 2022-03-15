# Nacar
# Copyright 2022 Alberto Morón Hernández
# [github.com/albertomh/Nacar]
#
# Test the FileIO module
# ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
# TODO: document

import os

import pytest
from yaml.scanner import ScannerError

from nacar.file_io import FileIO


#   Test `parse_yml_file()` ───────────────────────────────────────────────────

def test_parsing_inexistent_file():
    path_to_inexistent_file = '/tmp/inexistent-blueprint.yml'
    error_msg = f"The specified file '{path_to_inexistent_file}' does not exist."  # noqa

    with pytest.raises(FileNotFoundError, match=error_msg):
        FileIO.parse_yml_file(path_to_inexistent_file)


def test_parsing_invalid_yaml_in_existing_file():
    test_data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    path_to_invalid_yaml = os.path.join(test_data_dir, 'invalid-yaml.yml')  # noqa
    error_msg = f"Invalid YAML in '{os.path.abspath(path_to_invalid_yaml)}'. Please provide a blueprint that is valid YAML."  # noqa

    with pytest.raises(ScannerError, match=error_msg):
        FileIO.parse_yml_file(path_to_invalid_yaml)
