"""
Nacar
Copyright 2022 Alberto Morón Hernández
[github.com/albertomh/Nacar]

Blueprint translator interface
▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
TODO: document
"""

from abc import ABC, abstractmethod


class ITranslator(ABC):

    @abstractmethod
    def __init__(self, blueprint: dict) -> None:
        pass

    @abstractmethod
    def get_max_line_length(self) -> int:
        # Maximum line length in the target language. eg. 80 for Python.
        pass

    @abstractmethod
    def get_comment_lines(self, content: str) -> list:
        pass

    @abstractmethod
    def get_file_header(self) -> str:
        pass

    @abstractmethod
    def translate_blueprint(self) -> str:
        pass
