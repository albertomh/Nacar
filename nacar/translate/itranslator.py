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

from .target_language import TargetLanguage


class ITranslator(ABC):
    """
    __init__(blueprint: dict)

    <target_language> translator utilities
      ├ get_target_language() -> TargetLanguage
      ├ get_max_line_length() -> int
      ├ get_comment_lines(content: str) -> List[str]
      └ get_section_title(title: str) -> str

    File heading
      ├ get_title_lines() -> List[str]
      ├ get_copyright_lines() -> List[str]
      ├ get_nacar_info_lines() -> List[str]
      └ get_file_heading() -> str

    Nacar app config
      └ get_app_config() -> str

    Utilities
      └ get_utilities() -> str

    Translate blueprint to <target_language>
      └ translate_blueprint() -> str
    """

    @abstractmethod
    def __init__(self, blueprint: dict) -> None:
        pass

#   <target_language> translator utilities ─────────────────────────────────────

    @staticmethod
    @abstractmethod
    def get_target_language() -> TargetLanguage:
        raise NotImplementedError

    @abstractmethod
    def get_max_line_length(self) -> int:
        # Maximum line length in the target language. eg. 79 for Python.
        raise NotImplementedError

    @abstractmethod
    def get_comment_lines(self, content: str) -> List[str]:
        # Wrap lines to the max line length and make them comments.
        raise NotImplementedError

    @abstractmethod
    def get_section_title(self, title: str) -> str:
        # Print a title embedded in a horizontal rule.
        raise NotImplementedError

#   File heading ───────────────────────────────────────────────────────────────

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

#   Nacar app config ───────────────────────────────────────────────────────────

    @abstractmethod
    def get_app_config(self) -> str:
        # Nacar app settings eg. screen width, title.
        raise NotImplementedError

#   Utilities ──────────────────────────────────────────────────────────────────

    @abstractmethod
    def get_utilities(self) -> str:
        raise NotImplementedError

#   Translate blueprint ────────────────────────────────────────────────────────

    @abstractmethod
    def translate_blueprint(self) -> str:
        raise NotImplementedError
