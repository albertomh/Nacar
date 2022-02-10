#!/usr/bin/env python3

# Nacar
# Copyright 2022 Alberto Morón Hernández
# [github.com/albertomh/Nacar]

import io
from os.path import exists as file_exists

from yaml import safe_load
from yaml.scanner import ScannerError
from yaml.parser import ParserError


def load_data_from_file(file_path: str) -> dict:
    if not file_exists(file_path):
        raise FileNotFoundError(f"The specified file '{file_path}' does not exist.")

    invalid_yml_message = f"Invalid YAML in '{file_path}'. " \
                          f"Please provide a blueprint that is valid YAML."
    try:
        with io.open(file_path, 'r') as stream:
            data = safe_load(stream)
        return data
    except ScannerError:
        raise ScannerError(invalid_yml_message)
    except ParserError:
        raise ParserError(invalid_yml_message)


def main():
    try:
        print(load_data_from_file('yml/blueprint_example.yml'))
    except (FileNotFoundError, ScannerError, ParserError) as e:
        print(str(e))


if __name__ == '__main__':
    main()
