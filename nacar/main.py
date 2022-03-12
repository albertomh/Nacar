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
import os.path as os_path
from typing import Type, List

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
                 validator: NacarValidator,
                 translator_class: Type[ITranslator]):
        self.file_io = file_io
        self.schema = schema
        self.validator = validator
        self.translator_class = translator_class

    @staticmethod
    def get_blueprint_path_from_arguments(arguments: List[str]) -> str:
        try:
            # First argument passed must be the path to a blueprint.
            blueprint_path = arguments[1]
        except IndexError:
            raise IndexError("Please pass the path to a YAML blueprint as the first argument.")  # noqa

        blueprint_abspath = os_path.abspath(blueprint_path)
        if not os_path.isfile(blueprint_abspath):
            raise FileNotFoundError("The specified YAML blueprint does not exist.")  # noqa

        _, file_name = os_path.split(blueprint_abspath)
        if not (file_name.endswith('.yml') or file_name.endswith('.yaml')):
            raise RuntimeError("The specified blueprint does not seem to be a YAML document.")  # noqa

        return blueprint_path

    def run(self, blueprint_path):
        """
        Read and parse the given blueprint and validate it. If valid, output
        a Nacar script written in the Translator's TargetLanguage.
        :param blueprint_path: Path to the YAML blueprint to process.
        :return:
        """
        blueprint: dict

        try:
            blueprint = self.file_io.parse_yml_file(blueprint_path)
        except (FileNotFoundError, ScannerError) as e:
            print(str(e))
            return

        # Pass the blueprint schema to the Cerberus validator.
        try:
            blueprint_schema: dict = Schema.get_blueprint_schema()
        except (FileNotFoundError, ScannerError) as e:
            print(str(e))
            return

        # Validate the blueprint schema.
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

        try:
            translator: ITranslator = self.translator_class(blueprint)
            translation: str = translator.translate_blueprint()
        except (TypeError, NotImplementedError) as e:
            print(e)
            return

        # Write the Nacar app to a file that is a sibling of the blueprint.
        outdir, file_name = os_path.split(os_path.abspath(blueprint_path))
        blueprint_file_name, extension = os_path.splitext(file_name)
        try:
            FileIO.write_nacar_app_to_file(
                translation,
                os_path.join(outdir, blueprint_file_name),
                translator.get_target_language())
        except (NotImplementedError, FileNotFoundError) as e:
            print(e)
            return


def main():
    try:
        blueprint_path = Nacar.get_blueprint_path_from_arguments(argv)
    except (IndexError, FileNotFoundError, RuntimeError) as e:
        print(e)
        return

    if blueprint_path is not None:
        file_io = FileIO()
        schema = Schema()
        validator = NacarValidator()
        translator_class: Type[ITranslator] = BlueprintToBash
        nacar = Nacar(file_io, schema, validator, translator_class)

        try:
            nacar.run(blueprint_path)
        except InvalidSchemaError:
            print(f"'{os_path.abspath(blueprint_path)}' is not a valid "
                  f"blueprint. Please provide a blueprint that "
                  f"conforms to the schema.")


if __name__ == '__main__':
    main()
