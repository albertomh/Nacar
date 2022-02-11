#!/usr/bin/env python3

"""
Nacar
Copyright 2022 Alberto Morón Hernández
[github.com/albertomh/Nacar]

Application entrypoint
▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
TODO: document
"""

from sys import argv
from os.path import abspath

from yaml.scanner import ScannerError

from file_io import FileIO


class Nacar:
    def __init__(self, file_io):
        self.file_io = file_io

    def run(self, blueprint_path):
        try:
            blueprint: dict = self.file_io.parse_yml_file(blueprint_path)
            print(blueprint)  # TODO: remove.
        except (FileNotFoundError, ScannerError) as e:
            print(str(e))
            return


def main():
    # Two arguments must be present: `nacar.py` & a path to a blueprint.
    if len(argv) != 2:
        print("Please pass the filename of a YAML blueprint as Nacar's first argument.")  # noqa
        return

    file_io = FileIO()
    nacar = Nacar(file_io)

    blueprint_path = argv[1]
    nacar.run(blueprint_path)


if __name__ == '__main__':
    main()
