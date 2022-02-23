"""
Nacar
Copyright 2022 Alberto Morón Hernández
[github.com/albertomh/Nacar]

File IO utilities
▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
TODO: document
"""
import os
from os.path import exists as file_exists
from os.path import abspath

from yaml import safe_load
from yaml.scanner import ScannerError

from translate.target_language import TargetLanguage


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
            with open(file_path, 'r') as stream:
                data = safe_load(stream)
            return data
        except ScannerError:
            raise ScannerError(f"Invalid YAML in '{abspath(file_path)}'. Please provide a blueprint that is valid YAML.")  # noqa

    @staticmethod
    def write_nacar_app_to_file(script_content: str,
                                file_path: str,
                                target_language: TargetLanguage) -> None:
        if file_exists(file_path):
            os.remove(file_path)

        if target_language == TargetLanguage.BASH:
            with open(file_path, 'w') as outfile:
                outfile.write(script_content)

        else:
            raise NotImplementedError(f"There is no writer configured for "
                                      f"writing Nacar apps in "
                                      f"{target_language.name.title()}.")
