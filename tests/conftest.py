# Nacar
# Copyright 2022 Alberto Morón Hernández
# [github.com/albertomh/Nacar]
#
# Global test fixtures
# ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
# The test fixtures defined in this file are available
# to all test methods in the suite.

from os import path as os_path

import pytest


@pytest.fixture(scope='module')
def test_data_dir() -> str:
    return os_path.join(os_path.dirname(os_path.abspath(__file__)), 'data')
