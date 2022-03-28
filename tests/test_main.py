# Nacar
# Copyright 2022 Alberto Morón Hernández
# [github.com/albertomh/Nacar]
#
# Test Nacar's entrypoint
# ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
# Test parsing blueprint path from arguments, injecting dependencies,
# instantiating the Nacar class, and calling `run()` on it.

import os

import pytest

from nacar.file_io import FileIO
from nacar.schema import Schema
from nacar.validator import NacarValidator
from nacar.translate.to_bash.to_bash import BlueprintToBash
from nacar.main import Nacar


@pytest.fixture
def nacar() -> Nacar:
    file_io = FileIO()
    schema = Schema()
    validator = NacarValidator()
    return Nacar(file_io, schema, validator, BlueprintToBash)


@pytest.mark.parametrize('arguments,error_type,error_msg', [
    ([], IndexError, "Please pass the path to a YAML blueprint as the first argument."),  # noqa
    (['main.py'], IndexError, "Please pass the path to a YAML blueprint as the first argument."),  # noqa
    (['main.py', 'inexistent.yml'], FileNotFoundError, "The specified YAML blueprint does not exist."),  # noqa
    (['main.py', 'tests/data/valid-blueprint.json'], RuntimeError, "The specified blueprint does not seem to be a YAML document.")  # noqa
])
def test_get_blueprint_path_from_arguments(arguments: list, error_type, error_msg: str):
    with pytest.raises(error_type, match=error_msg):
        Nacar.get_blueprint_path_from_arguments(arguments)


def test_success_message(capsys, test_data_dir, nacar: Nacar):
    path_to_blueprint = os.path.join(test_data_dir, 'valid-blueprint.yml')
    nacar.run(path_to_blueprint)
    captured = capsys.readouterr()
    assert captured.out == "\nConverted blueprint 'valid-blueprint.yml' to bash Nacar app 'valid-blueprint'. Wrote 258 lines.\n\n"  # noqa
    os.remove(os.path.join(test_data_dir, 'valid-blueprint'))
