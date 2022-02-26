"""
Nacar
Copyright 2022 Alberto Morón Hernández
[github.com/albertomh/Nacar]

Blueprint to bash translator
▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔
TODO: document
"""

import os
import sys
# Add `translate` module to path so ITranslator import may be performed.
from typing import List, Union
from datetime import datetime
import textwrap

# Add root Nacar package to syspath to make below imports possible.
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))  # noqa
from __version__ import __version__
from translate.itranslator import ITranslator
from translate.target_language import TargetLanguage


class BlueprintToBash(ITranslator):
    """
    [I] indicates a method implements the interface's definition.

    ╶ __init__()

    Bash translator utilities
      ├ [I] get_target_language() -> TargetLanguage
      ├ [I] get_max_line_length() -> str
      ├ [I] get_comment_lines(content: str) -> List[str]
      └ [I] get_section_title(title: str) -> str

    File heading
      ├     get_hashbang_lines() -> List[str]
      ├ [I] get_title_lines() -> List[str]
      ├ [I] get_copyright_lines() -> List[str]
      ├ [I] get_nacar_info_lines() -> List[str]
      └ [I] get_file_heading() -> str

    Utilities
      ├     get_bash_styles_lines() -> List[str]
      ├     get_clear_screen_lines() -> List[str]
      ├     get_repeat_method_lines() -> List[str]
      └ [I] get_utilities() -> str

    Translate blueprint to Bash
      └ [I] translate_blueprint() -> str
    """

    def __init__(self, blueprint: dict):
        self.blueprint = blueprint

#   Bash translator utilities ──────────────────────────────────────────────────

    @staticmethod
    def get_target_language() -> TargetLanguage:
        return TargetLanguage.BASH

    def get_max_line_length(self):
        return 80

    def get_comment_lines(self, content: Union[str, List[str]]) -> List[str]:
        if len(content) == 0:
            return ["#"]

        comment_lines: List[str] = []
        if type(content) is str:
            width = self.get_max_line_length() - 2
            comment_lines = textwrap.wrap(content, width)
        elif type(content) is list:
            comment_lines = content

        return [f"# {c}" for c in comment_lines]

    def get_section_title(self, title: str, rule_char='─') -> str:
        len_right = self.get_max_line_length() - (2 + 5 + 1 + len(title) + 1)
        return f"# {rule_char * 5} {title} {rule_char * len_right}"

#   File heading ───────────────────────────────────────────────────────────────

    def get_hashbang_lines(self) -> List[str]:
        return ["#!/bin/bash", ""]

    def get_title_lines(self) -> List[str]:
        return self.get_comment_lines(self.blueprint['title'])

    def get_copyright_lines(self) -> List[str]:
        copyright_lines = []

        authors: list = self.blueprint['meta']['authors']
        if len(authors) > 0:
            current_year = datetime.now().year

            copyright_lines.append(f"# Copyright {current_year}")

            for counter, a in enumerate(authors):
                # TODO: simplify with a call to self.get_comment_lines()
                last_line = copyright_lines[-1]
                new_last_line = last_line
                # Add a comma between each author's name
                if 0 < counter < (len(authors) + 1):
                    new_last_line += ","
                # Ensure lines don't overrun the screen width.
                if len(f"{new_last_line} {a}") > self.get_max_line_length():
                    copyright_lines.append(f"# {a}")
                else:
                    copyright_lines[-1] = f"{new_last_line} {a}"

        return copyright_lines

    def get_nacar_info_lines(self) -> List[str]:
        today = datetime.now().date().isoformat()
        info = f"Generated by Nacar {__version__} on {today}."
        gh_info = "[github.com/albertomh/Nacar]"

        return self.get_comment_lines([info, gh_info])

    def get_file_heading(self) -> str:
        file_header_lines = []
        file_header_lines += self.get_hashbang_lines()
        file_header_lines += self.get_title_lines()
        file_header_lines += self.get_copyright_lines()
        file_header_lines += self.get_comment_lines("")
        file_header_lines += self.get_nacar_info_lines()
        file_header_lines += ["\n"]

        return '\n'.join(file_header_lines)

#   Nacar app config ───────────────────────────────────────────────────────────

    def get_app_config(self) -> str:
        config_lines = [self.get_section_title('Nacar app config')]
        config_lines += [""]
        config_lines += [f"SCREEN_WIDTH={self.blueprint['meta']['width']}"]
        config_lines += [f"TITLE={self.blueprint['title']}"]
        config_lines += ["", "", ""]

        return '\n'.join(config_lines)

#   Utilities ──────────────────────────────────────────────────────────────────

    def get_bash_styles_lines(self) -> List[str]:
        # [gist.github.com/vratiu/9780109]
        styles = {
            'BLD': r"$'\e[1m'",
            'DIM': r"$'\e[2m'",
            'UND': r"$'\e[4m'",

            'RED': r"$'\e[1;91m'",
            'GRN': r"$'\e[1;32m'",
            'YEL': r"$'\e[1;93m'",
            'BLU': r"$'\e[1;34m'",
            'END': r"$'\e[0m'"
        }

        styles_lines = []
        for name, code in styles.items():
            styles_lines.append(f"{name}={code}")

        return styles_lines

    def get_clear_screen_lines(self) -> List[str]:
        return [
            "clear_screen() {",
            "    printf " r'"\033c"',
            "}"
        ]

    def get_repeat_method_lines(self) -> List[str]:
        repeat_method = []
        repeat_method += self.get_comment_lines([
            "Use: `repeat '-' 76`",
            "@param $1 The string to repeat.",
            "@param $2 How many times to repeat it."
        ])

        repeat_method += [
            r"repeat() {",
            r'	  for i in $(seq 1 $2); do printf "$1"; done',
            r"}"
        ]

        return repeat_method

    def get_utilities(self) -> str:
        utilities_lines = [self.get_section_title('Utilities')]
        utilities_lines += [""]
        utilities_lines += self.get_bash_styles_lines()
        utilities_lines += [""]
        utilities_lines += self.get_clear_screen_lines()
        utilities_lines += [""]
        utilities_lines += self.get_repeat_method_lines()
        utilities_lines += ["\n"]

        return '\n'.join(utilities_lines)

#   Translate blueprint to Bash ────────────────────────────────────────────────

    def translate_blueprint(self) -> str:
        """
        Given a blueprint (a Python object built by parsing a YAML blueprint),
        return a string containing the blueprint's translation to Bash, ready
        to be persisted to a file and used as a Nacar application.
        """

        bash_translation = self.get_file_heading()
        bash_translation += self.get_app_config()
        bash_translation += self.get_utilities()

        return bash_translation
