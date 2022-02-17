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
from schema import Schema, InvalidSchemaError
from validator import NacarValidator
from translate.itranslator import ITranslator
from translate.to_bash.to_bash import BlueprintToBash


class Nacar:
    def __init__(self,
                 file_io: FileIO,
                 schema: Schema,
                 validator: NacarValidator):
        self.file_io = file_io
        self.schema = schema
        self.validator = validator

    def run(self, blueprint_path):
        """
        Read and parse the given blueprint and output a bash script.
        :param blueprint_path: Path to the YAML blueprint to process.
        :return:
        """
        blueprint: dict

        try:
            blueprint = self.file_io.parse_yml_file(blueprint_path)
        except (FileNotFoundError, ScannerError) as e:
            print(str(e))
            return

        try:
            blueprint_schema: dict = Schema.get_blueprint_schema()
        except (FileNotFoundError, ScannerError) as e:
            print(str(e))
            return

        try:
            schema_is_valid: bool = (self.validator
                                     .validate(blueprint, blueprint_schema))
        except RuntimeError as e:
            print(e)
            return
        if not schema_is_valid:
            raise InvalidSchemaError(self.validator.errors)

        # TODO: add more defaults to the below method.
        blueprint = self.schema.set_missing_optional_attributes(blueprint)

        translator: ITranslator = BlueprintToBash(blueprint)
        print(translator.translate_blueprint())  # TODO: remove.


def main():
    # Two arguments must be present: `nacar.py` & a path to a blueprint.
    if len(argv) != 2:
        print("Please pass the filename of a YAML blueprint as Nacar's first argument.")  # noqa
        return

    file_io = FileIO()
    schema = Schema()
    validator = NacarValidator()
    nacar = Nacar(file_io, schema, validator)

    blueprint_path = argv[1]
    try:
        nacar.run(blueprint_path)
    except InvalidSchemaError:
        print(f"'{abspath(blueprint_path)}' is not a valid blueprint. "
              f"Please provide a blueprint that conforms to the schema.")


if __name__ == '__main__':
    main()
