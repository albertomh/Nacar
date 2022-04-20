"""
Nacar
Copyright 2022 Alberto Morón Hernández
[github.com/albertomh/Nacar]

Blueprint to bash translator
▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
Implements the ITranslator interface to turn blueprints into bash Nacar apps.
Find out more about translators by reading `/docs/Translators.md`.
"""

from os.path import dirname, abspath
from typing import List
from datetime import datetime

from nacar.__version__ import __version__
from nacar.schema import Schema
from nacar.translate.itranslator import ITranslator
from nacar.translate.target_language import TargetLanguage


class BlueprintToBash(ITranslator):
    """
    template_data: dict
    set_template_data(data: dict) -> None
    screens: List[str]
    set_screens() -> None
    __init__(blueprint: dict) -> None

    Bash translator utilities
      ├ get_target_language() -> TargetLanguage
      ├ get_comment_lines(content: str) -> List[str]
      └ get_section_title(title: str) -> str

    File heading
      └ set_heading_template_variables() -> None

    Utilities
      ├ get_bash_styles() -> dict
      └ set_utilities_template_variables() -> None

    Screen-building utilities
      └ set_screen_building_utilities() -> None

    Screen-rendering code
      └ set_screen_rendering_template_variables() -> None

    Nacar app's main loop
      └ set_main_loop_code_template_variables() -> None

    Translate blueprint to Bash
      └ translate_blueprint() -> str
    """

    template_data: dict = {}

    def set_template_data(self, data: dict) -> None:
        self.template_data = data

    screens: List[str] = []

    def set_screens(self) -> None:
        self.screens = Schema.get_screen_names(self.blueprint)

    def __init__(self, blueprint: dict) -> None:
        translator_dir = dirname(abspath(__file__))
        super().__init__(blueprint, translator_dir)

#   Bash translator utilities ─────────────────────────────────────────────────

    @staticmethod
    def get_target_language() -> TargetLanguage:
        return TargetLanguage.BASH

#   File heading ──────────────────────────────────────────────────────────────

    def set_heading_template_variables(self) -> None:
        """
        Set data used to render the title, copyright, year, and authors.
        """

        heading_data = {
            'title': self.blueprint['title'],
            'current_year': datetime.now().year,
            'authors': ', '.join(self.blueprint['meta']['authors']),
            'nacar_version': __version__,
            'current_date': datetime.now().date().isoformat()
        }
        self.set_template_data({
            **self.template_data,
            **{'heading': heading_data}
        })

#   Nacar app config ──────────────────────────────────────────────────────────

    def set_app_config_template_variables(self) -> None:
        app_config_data = {
            'screen_width': self.blueprint['meta']['width']
        }
        self.set_template_data({
            **self.template_data,
            **{'app_config': app_config_data}
        })

#   Utilities ─────────────────────────────────────────────────────────────────

    def get_bash_styles(self) -> dict:
        # [gist.github.com/vratiu/9780109]
        return {
            'BLD': r"$'\e[1m'",
            'DIM': r"$'\e[2m'",
            'UND': r"$'\e[4m'",

            'RED': r"$'\e[1;91m'",
            'GRN': r"$'\e[1;32m'",
            'YEL': r"$'\e[1;93m'",
            'BLU': r"$'\e[1;34m'",
            'END': r"$'\e[0m'"
        }

    def set_utilities_template_variables(self) -> None:
        utilities_data = {
            'bash_styles': self.get_bash_styles()
        }
        self.set_template_data({
            **self.template_data,
            **{'utilities': utilities_data}
        })

#   Screen flow ───────────────────────────────────────────────────────────────

    def set_screen_flow_template_variables(self) -> None:
        screen_options = {}
        for screen in self.screens:
            options = Schema.get_options_for_screen(self.blueprint, screen)
            screen_options[screen] = options

        screen_flow_data = {
            'screens': self.screens,
            'screen_options': screen_options,
        }
        self.set_template_data({
            **self.template_data,
            **{'screen_flow': screen_flow_data}
        })

#   Screen rendering ──────────────────────────────────────────────────────────

    def set_screen_rendering_template_variables(self) -> None:
        bottom_padding_screen_map = {}
        for screen in self.screens:
            options = Schema.get_options_for_screen(self.blueprint, screen)
            max_options = Schema.get_max_screen_options_in_blueprint(self.blueprint)  # noqa
            bottom_padding = 1 + (max_options - len(options))
            bottom_padding_screen_map[screen] = bottom_padding

        screen_rendering_data = {
            'show_made_with_on_exit': self.blueprint['meta']['show_made_with_on_exit'],  # noqa
            'bottom_padding_screen_map': bottom_padding_screen_map
        }
        self.set_template_data({
            **self.template_data,
            **{'screen_rendering': screen_rendering_data}
        })

#   Translate blueprint to Bash ───────────────────────────────────────────────

    def translate_blueprint(self) -> str:
        """
        Given a blueprint (a Python object built by parsing a YAML blueprint),
        return a string containing the blueprint's translation to Bash, ready
        to be persisted to a file and used as a Nacar application.
        """

        self.set_heading_template_variables()
        self.set_app_config_template_variables()
        self.set_utilities_template_variables()
        self.set_screen_flow_template_variables()
        self.set_screen_rendering_template_variables()

        template = self.jinja_env.get_template('base.sh.template')
        bash_translation: str = template.render(self.template_data)

        return bash_translation
