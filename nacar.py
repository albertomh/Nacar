#!/usr/bin/env python3

# Nacar
# Copyright 2022 Alberto Morón Hernández
# [github.com/albertomh/Nacar]

import io
from os.path import exists as file_exists

from yaml import safe_load
from yaml.scanner import ScannerError


def load_data_from_file(file_path: str) -> dict:
    if not file_exists(file_path):
        raise FileNotFoundError(f"The specified file '{file_path}' does not exist.")

    try:
        with io.open(file_path, 'r') as stream:
            data = safe_load(stream)
        return data
    except ScannerError as e:
        raise ScannerError(f"Invalid YAML in '{file_path}'. "
            "Please provide a blueprint that is valid YAML.")


def main():
    print(load_data_from_file('yml/blueprint_example.yml'))


if __name__ == '__main__':
    main()
