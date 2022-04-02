"""
Nacar
Copyright 2022 Alberto Morón Hernández
[github.com/albertomh/Nacar]

Blueprint translator interface
▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
Translators are packages that take a Python object and turn it into a Nacar
application written in a target language such as Bash. The `itranslator.py`
interface defines the methods a translator should implement.
Find out more about translators by reading `/docs/Translators.md`.
"""

from os import path as os_path
from abc import ABC, abstractmethod
from typing import List

from jinja2 import Environment, FileSystemLoader

from nacar.translate.target_language import TargetLanguage


class ITranslator(ABC):
    """
    template_data: dict
    set_template_data(data: dict) -> None
    screens: List[str]
    set_screens() -> None
    __init__(blueprint: dict) -> None

    <target_language> translator utilities
      ├ get_target_language() -> TargetLanguage
      └ get_max_line_length() -> int

    File heading
      └ set_heading_template_variables() -> None
    """

    @property
    @abstractmethod
    def template_data(self) -> dict:
        # A dictionary containing all data necessary to
        # generate the application using templates.
        raise NotImplementedError

    @abstractmethod
    def set_template_data(self, data: dict) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def screens(self) -> List[str]:
        # A list of screen names as defined by the blueprint.
        raise NotImplementedError

    def __init__(self, blueprint: dict, translator_dir: str) -> None:
        self.blueprint = blueprint
        self.set_screens()

        templates_dir = os_path.join(translator_dir, 'templates')
        self.jinja_env = Environment(loader=FileSystemLoader(templates_dir))
        self.jinja_env.trim_blocks = True
        self.jinja_env.lstrip_blocks = True

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
    def set_screens(self) -> None:
        # Set the Translator's `screens` field.
        raise NotImplementedError

#   File heading ───────────────────────────────────────────────────────────────

    @abstractmethod
    def set_heading_template_variables(self) -> None:
        raise NotImplementedError

#   Nacar app config ───────────────────────────────────────────────────────────

    @abstractmethod
    def set_app_config_template_variables(self) -> None:
        # Nacar app settings eg. screen width, title.
        raise NotImplementedError

#   Utilities ──────────────────────────────────────────────────────────────────

    @abstractmethod
    def get_utilities(self) -> str:
        raise NotImplementedError

#   Screen-building utilities ──────────────────────────────────────────────────

    @abstractmethod
    def get_screen_building_utilities(self) -> str:
        raise NotImplementedError

#   Screen flow ────────────────────────────────────────────────────────────────

    @abstractmethod
    def get_screen_flow_code(self) -> str:
        raise NotImplementedError

#   Screen rendering ───────────────────────────────────────────────────────────

    @abstractmethod
    def get_screen_rendering_code(self) -> str:
        raise NotImplementedError

#   Nacar app's main loop ──────────────────────────────────────────────────────

    @abstractmethod
    def get_main_loop_code(self) -> str:
        raise NotImplementedError

#   Translate blueprint ────────────────────────────────────────────────────────

    @abstractmethod
    def translate_blueprint(self) -> str:
        raise NotImplementedError
