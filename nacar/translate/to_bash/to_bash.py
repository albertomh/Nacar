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


class BlueprintToBash(ITranslator):
    """
    ╶ __init__()

    Bash translator utilities
      ├ get_max_line_length() -> str
      └ get_comment_lines(content: str) -> List[str]

    File heading
      ├ get_hashbang_lines() -> List[str]
      ├ get_title_lines() -> List[str]
      ├ get_copyright_lines() -> List[str]
      ├ get_nacar_info_lines() -> List[str]
      └ get_file_heading() -> str

    Translate blueprint to Bash
      └ translate_blueprint() -> str
    """

    def __init__(self, blueprint: dict):
        self.blueprint = blueprint

#   Bash translator utilities ──────────────────────────────────────────────────

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

#   Translate blueprint to Bash ────────────────────────────────────────────────

    def translate_blueprint(self) -> str:
        """
        Given a blueprint (a Python object built by parsing a YAML blueprint),
        return a string containing the blueprint's translation to Bash, ready
        to be persisted to a file and used as a Nacar application.
        """

        bash_translation = self.get_file_heading()

        return bash_translation
