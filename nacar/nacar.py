#!/usr/bin/env python3

# Nacar
# Copyright 2022 Alberto Morón Hernández
# [github.com/albertomh/Nacar]

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
    file_io = FileIO()
    nacar = Nacar(file_io)

    nacar.run('yml/blueprint_example.yml')


if __name__ == '__main__':
    main()
