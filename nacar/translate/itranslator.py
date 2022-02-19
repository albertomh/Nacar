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
    ╶ __init__(blueprint: dict)

    <target_language> translator utilities
      ├ get_max_line_length() -> int
      └ get_comment_lines(content: str) -> List[str]

    File heading
      ├ get_title_lines() -> List[str]
      ├ get_copyright_lines() -> List[str]
      ├ get_nacar_info_lines() -> List[str]
      └ get_file_heading() -> str

    Translate blueprint to <target_language>
      └ translate_blueprint() -> str
    """

    @abstractmethod
    def __init__(self, blueprint: dict) -> None:
        pass

#   <target_language> translator utilities ─────────────────────────────────────

    @abstractmethod
    def get_max_line_length(self) -> int:
        # Maximum line length in the target language. eg. 79 for Python.
        raise NotImplementedError

    @abstractmethod
    def get_comment_lines(self, content: str) -> List[str]:
        raise NotImplementedError

#   File header ────────────────────────────────────────────────────────────────

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

#   Translate blueprint ────────────────────────────────────────────────────────

    @abstractmethod
    def translate_blueprint(self) -> str:
        raise NotImplementedError
