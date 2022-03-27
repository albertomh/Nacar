# Nacar
# Copyright 2022 Alberto Morón Hernández
# [github.com/albertomh/Nacar]
#
# Test Nacar's entrypoint
# ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
# Test parsing blueprint path from arguments, injecting dependencies,
# instantiating the Nacar class, and calling `run()` on it.

import pytest

from nacar.main import Nacar


@pytest.mark.parametrize('arguments,error_type,error_msg', [
    ([], IndexError, "Please pass the path to a YAML blueprint as the first argument."),  # noqa
    (['main.py'], IndexError, "Please pass the path to a YAML blueprint as the first argument."),  # noqa
    (['main.py', 'inexistent.yml'], FileNotFoundError, "The specified YAML blueprint does not exist."),  # noqa
    (['main.py', 'tests/data/valid-blueprint.json'], RuntimeError, "The specified blueprint does not seem to be a YAML document.")  # noqa
])
def test_get_blueprint_path_from_arguments(arguments: list, error_type, error_msg: str):
    with pytest.raises(error_type, match=error_msg):
        Nacar.get_blueprint_path_from_arguments(arguments)
