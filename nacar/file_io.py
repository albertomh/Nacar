#!/usr/bin/env python3

"""
Nacar
Copyright 2022 Alberto Morón Hernández
[github.com/albertomh/Nacar]

File IO utilities
▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
TODO: document
"""

import io
from os.path import exists as file_exists
from os.path import abspath

from yaml import safe_load
from yaml.scanner import ScannerError


class FileIO:

    @staticmethod
    def parse_yml_file(file_path: str) -> dict:
        """
        Read and parse a YML file, representing its contents as a dictionary.
        :param file_path: Relative to the project's root directory.
        :return: A dictionary built from the YML object.
        """

        if not file_exists(file_path):
            raise FileNotFoundError(f"The specified file '{abspath(file_path)}' does not exist.")  # noqa

        try:
            with io.open(file_path, 'r') as stream:
                data = safe_load(stream)
            return data
        except ScannerError:
            raise ScannerError(f"Invalid YAML in '{abspath(file_path)}'. Please provide a blueprint that is valid YAML.")  # noqa
