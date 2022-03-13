"""
Nacar
Copyright 2022 Alberto Morón Hernández
[github.com/albertomh/Nacar]

Target Languages enumeration
▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
Used to identify Translators and to ensure the file_io module
knows how to write out to a file of the specified type.
"""

from enum import Enum


class TargetLanguage(Enum):
    BASH = 1
