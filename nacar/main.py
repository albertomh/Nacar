#!/usr/bin/env python3

"""
Nacar
Copyright 2022 Alberto Morón Hernández
[github.com/albertomh/Nacar]

Application entrypoint
▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
Nacar's entrypoint when it is run from the command line. Responsible for
running initial checks, catching any exceptions, and orchestrating core
functionalities - read YAML blueprints, parse to in-memory object,
translate, and finally write to file.
"""

from sys import argv
import os.path as os_path
from typing import Type, List

from yaml.scanner import ScannerError

from nacar.file_io import FileIO
from nacar.schema import Schema, InvalidSchemaError
from nacar.validator import NacarValidator
from nacar.translate.itranslator import ITranslator
from nacar.translate.target_language import TargetLanguage
from nacar.translate.to_bash.to_bash import BlueprintToBash


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
            blueprint: dict = self.file_io.parse_yml_file(blueprint_path)
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

        blueprint = self.schema.set_missing_optional_attributes(blueprint)

        # Translate the in-memory blueprint to a Nacar app (as a string).
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

        # Print out a message to signal successful execution.
        success_message = f"\nConverted blueprint '{file_name}' to "

        if translator.get_target_language() == TargetLanguage.BASH:
            success_message += f"bash Nacar app '{blueprint_file_name}'."
            with open(os_path.join(outdir, blueprint_file_name)) as app:
                success_message += f" Wrote {len(app.readlines()) + 1} lines."

        print(f"{success_message}\n")


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
        # The only translator for the time being is the Bash Translator.
        translator_class: Type[ITranslator] = BlueprintToBash
        nacar = Nacar(file_io, schema, validator, translator_class)

        try:
            nacar.run(blueprint_path)
        except InvalidSchemaError as err:
            print(f"'{os_path.abspath(blueprint_path)}' is not a valid blueprint.")  # noqa
            print(f"{err.message}")


if __name__ == '__main__':
    main()
