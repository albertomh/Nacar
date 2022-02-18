"""
Nacar
Copyright 2022 Alberto Morón Hernández
[github.com/albertomh/Nacar]

Blueprint translator interface
▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
TODO: document
"""

from abc import ABC, abstractmethod
from typing import List


class ITranslator(ABC):
    """
    """

    @abstractmethod
    def __init__(self, blueprint: dict) -> None:
        pass

#   0. Bash translator utilities -----------------------------------------------

    @abstractmethod
    def get_max_line_length(self) -> int:
        # Maximum line length in the target language. eg. 79 for Python.
        raise NotImplementedError

    @abstractmethod
    def get_comment_lines(self, content: str) -> List[str]:
        raise NotImplementedError

#   1. File header -------------------------------------------------------------

    @abstractmethod
    def get_title_lines(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_copyright_lines(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_nacar_info_lines(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_file_heading(self) -> str:
        raise NotImplementedError
