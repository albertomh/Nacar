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
from schema import Schema
from translate.itranslator import ITranslator
from translate.target_language import TargetLanguage


class BlueprintToBash(ITranslator):
    """
    [I] indicates that a method implements the interface's definition.

    screens: List[str]
    __init__(blueprint: dict) -> None

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

    Screen-building utilities
      ├     get_print_blank_screen_line_method_lines() -> List[str]
      ├     get_print_screen_top_method_lines() -> List[str]
      ├     get_print_breadcrumbs_method_lines() -> List[str]
      ├     get_print_screen_bottom_method_lines() -> List[str]
      └ [I] get_screen_building_utilities() -> str

    Screen flow
      ├     get_screen_flow_state_variables_lines() -> List[str]
      ├     get_screen_flow_constants_lines() -> List[str]
      ├     get_navigate_to_method_lines() -> List[str]
      ├     get_navigate_back_method_lines() -> List[str]
      ├     get_show_active_screen_method_lines() -> List[str]
      ├     get_check_keystroke_method_lines() -> List[str]
      └ [I] get_screen_flow_code() -> str

    Screen rendering
      ├     get_invoke_action_on_exit_lines() -> List[str]
      ├     get_show_exit_screen_lines() -> List[str]
      └ [I] get_screen_rendering_code() -> str

    Nacar app's main loop
      └ [I] get_main_loop_code() -> str

    Translate blueprint to Bash
      └ [I] translate_blueprint() -> str
    """

    screens: List[str] = []

    def __init__(self, blueprint: dict) -> None:
        self.blueprint = blueprint
        self.set_screens()

#   Bash translator utilities ──────────────────────────────────────────────────

    @staticmethod
    def get_target_language() -> TargetLanguage:
        return TargetLanguage.BASH

    def get_max_line_length(self):
        return 80

    def set_screens(self):
        self.screens = Schema.get_screen_names(self.blueprint)

    def get_comment_lines(self, content: Union[str, List[str]], lpad=0) -> List[str]:  # noqa
        if len(content) == 0:
            return ["#"]

        comment_lines: List[str] = []
        if type(content) is str:
            width = self.get_max_line_length() - 2
            comment_lines = textwrap.wrap(content, width)
        elif type(content) is list:
            comment_lines = content

        return [f"{' ' * lpad}# {c}" for c in comment_lines]

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
        """
        Add the hashbang and a comment with the copyright, year, and authors.
        :return:
        """
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
        config_lines += [f"TITLE=\"{self.blueprint['title']}\""]
        config_lines += ["\n\n"]

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
        utilities_lines += ["\n\n"]

        return '\n'.join(utilities_lines)

#   Screen-building utilities ──────────────────────────────────────────────────

    def get_print_blank_screen_line_method_lines(self) -> List[str]:
        blank_screen_method = []
        blank_screen_method += self.get_comment_lines(
            "@param $1 Optional number of blank lines to print. Defaults to one."  # noqa
        )
        blank_screen_method += [
            r'print_blank_screen_line() {',
            r'    local spaces_count=$(($SCREEN_WIDTH - 4))',
            r'    if [[ $# -eq 0 ]]; then',
            r'        printf "\U2502 %${spaces_count}s \U2502\n"',
            r'    else',
            r'        for i in $(seq 1 $1); do printf "\U2502 %${spaces_count}s \U2502\n"; done',  # noqa
            r'    fi',
            r'}'
        ]
        return blank_screen_method

    def get_print_screen_top_method_lines(self) -> List[str]:
        return [
            r'print_screen_top() {',
            r'    local title_charlen=${#TITLE}',
            r'    local topline_width=$(($SCREEN_WIDTH - (2 + $title_charlen + 2)))',  # noqa
            r'    local topline_width_left=$(($topline_width / 2))',
            r'    local topline_width_right=$(($topline_width_left + ($topline_width % 2)))',  # noqa
            "",
            r'''    printf "\U256D%s $TITLE %s\U256E\n" $(repeat '\U2500' $topline_width_left) $(repeat '\U2500' $topline_width_right)''',  # noqa
            "",
            r'    if [[ ${ACTIVE_SCREEN} == ${HOME_SCREEN} ]]; then',
            r'        local left_margin=$((SCREEN_WIDTH - 10))',
            r'        printf "\U2502 %${left_margin}s [${RED}ESC${END}] \U2502\n"',  # noqa
            r'    else',
            r'        local inner_margin=$((SCREEN_WIDTH - 15))',
            r'        printf "\U2502 [${BLU}\U25C0${END} ] %${inner_margin}s [${RED}ESC${END}] \U2502\n"',  # noqa
            r'    fi',
            r'    print_blank_screen_line',
            r'    print_breadcrumbs',
            r'    print_blank_screen_line',
            r'}'
        ]

    def get_print_breadcrumbs_method_lines(self) -> List[str]:
        return [
            r'print_breadcrumbs() {',
            r'    if [[ ! ${ACTIVE_SCREEN} ]]; then',
            r'        return 1;',
            r'    fi',
            "",
            r'    local breadcrumbs_str',
            r'    local breadcrumbs_count="${#BREADCRUMBS[@]}"',
            r'    local breadcrumbs_str=""',
            r'    local delimiter=""',
            r'    local breadcrumbs_width=0',
            r'    local crumb_counter=0',
            r'    for crumb in "${BREADCRUMBS[@]}"; do',
            r'        crumb_counter=$((crumb_counter + 1))',
            r'        if [[ $crumb_counter -eq $breadcrumbs_count ]]; then',
            r'            crumb="${UND}$crumb${END}"',
            r'        else',
            r'            crumb="${DIM}$crumb${END}"',
            r'        fi',
            r'        breadcrumbs_str="$breadcrumbs_str$delimiter$crumb"',
            r'        crumb_len=${#crumb}',
            r'        breadcrumbs_width=$((breadcrumbs_width + crumb_len))',
            r'        delimiter=" \U203A "',
            r'    done',
            "",
            r'    local surrounding_width=4  # Pipes and spaces around breadcrumbs.',  # noqa
            r'    local chevrons_width=$(((breadcrumbs_count - 1) * 3))',
            r'    local style_buffer=$((breadcrumbs_count * 8))',
            r'    local breadcrumbs_str_len=$((breadcrumbs_width + chevrons_width))',  # noqa
            "",
            r'    local right_pad=$((SCREEN_WIDTH - (breadcrumbs_str_len + surrounding_width)))',  # noqa
            r'    right_pad=$((right_pad + style_buffer))',
            r'    printf "\U2502 ${breadcrumbs_str}%${right_pad}s \U2502\n"',
            r'}'
        ]

    def get_print_screen_bottom_method_lines(self) -> List[str]:
        screen_bottom_lines = []
        screen_bottom_lines += self.get_comment_lines(
            "@param $1 Optional number of blank lines before the bottom. Defaults to one."  # noqa
        )
        screen_bottom_lines += [
            r'print_screen_bottom() {',
            r'    local preBottomBlankLines=1',
            r'    if [[ $# -ne 0 ]]; then preBottomBlankLines=$1; fi',
            "",
            r'    print_blank_screen_line $preBottomBlankLines',
            r'    local bottom_width=$((SCREEN_WIDTH - 2))',
            r'''    printf "\U2570%s\U256F\n" $(repeat '\U2500' $bottom_width)''',  # noqa
            r'}'
        ]
        return screen_bottom_lines

    def get_screen_building_utilities(self) -> str:
        screen_building_lines = [self.get_section_title('Screen-building utilities')]  # noqa
        screen_building_lines += [""]
        screen_building_lines += self.get_print_blank_screen_line_method_lines()
        screen_building_lines += [""]
        screen_building_lines += self.get_print_screen_top_method_lines()
        screen_building_lines += [""]
        screen_building_lines += self.get_print_breadcrumbs_method_lines()
        screen_building_lines += [""]
        screen_building_lines += self.get_print_screen_bottom_method_lines()
        screen_building_lines += ["\n\n"]

        return '\n'.join(screen_building_lines)

#   Screen flow ────────────────────────────────────────────────────────────────

    def get_screen_flow_state_variables_lines(self) -> List[str]:
        return [
            r'declare -a BREADCRUMBS=()',
            r'# The name of the screen to show. One of the `_SCREEN` constants below.',  # noqa
            r'ACTIVE_SCREEN=""',
            r'# The command to invoke on exit.',
            r'INVOKE_ON_EXIT=""'
        ]

    def get_screen_flow_constants_lines(self) -> List[str]:
        constants_lines = []

        for screen in self.screens:
            constants_lines += [fr'readonly {screen.upper()}_SCREEN="{screen.lower()}"']  # noqa

        return constants_lines

    def get_navigate_to_method_lines(self) -> List[str]:
        return [
            r'navigate_to() {',
            r'    INVOKE_ON_EXIT=""',
            r'    ACTIVE_SCREEN="$1"',
            r'    BREADCRUMBS+=("$1")',
            r'}'
        ]

    def get_navigate_back_method_lines(self) -> List[str]:
        return [
            r'# Remove last element of BREADCRUMBS.',
            r'navigate_back() {',
            r'    if [[ ${#BREADCRUMBS[@]} -eq 1 ]]; then',
            r'        :  # Prevent navigating back when on homescreen.',
            r'    else',
            "        unset 'BREADCRUMBS[-1]'  # Remove current screen.",
            r'        local previous_screen=${BREADCRUMBS[-1]}',
            r'        # Remove previous screen since it will be added back by `navigate_to`.',  # noqa
            "        unset 'BREADCRUMBS[-1]'",
            r'        navigate_to ${previous_screen}',
            r'    fi',
            r'}'
        ]

    def get_show_active_screen_method_lines(self) -> List[str]:
        return [
            r'show_active_screen() {',
            r'    # There should always be an active screen, exit if not.',
            r'    if [[ ! ${ACTIVE_SCREEN} ]]; then return 1; fi',
            "",
            r'    clear_screen',
            r'    eval "show_${ACTIVE_SCREEN}_screen"',
            r'}'
        ]

    def get_check_keystroke_method_lines(self) -> List[str]:
        check_keystroke_lines = self.get_comment_lines([
            "@param $1 The screen this function is invoked from.",
            "          One of the _SCREEN constants declared above."
        ])
        check_keystroke_lines += [
            r'check_keystroke() {',
            r'    local prompt=" ${GRN}\$${END}"',
            r'    read -rs -p " ${prompt} " -n1 key',
            r''
        ]

        # Dynamically build case statements on a per-screen basis
        # to handle keystrokes indicating option selection.
        check_keystroke_lines += self.get_comment_lines([
            "Keypresses related to a screen."
        ], 4)
        screen_case_lines = []

        for i, screen in enumerate(self.screens):
            conditional_keyword = 'if' if i == 0 else 'elif'
            screen_case_lines += [
                fr'    {conditional_keyword} [[ "$1" == "${screen.upper()}_SCREEN" ]]; then'  # noqa
            ]
            # Loop over the actions and/or links defined for this screen.
            screen_case_lines += [r'        case "$key" in']
            options = Schema.get_options_for_screen(self.blueprint, screen)  # noqa
            for option in options:
                key: str = option['name'][0]
                screen_case_lines += [fr'            "{key.upper()}" | "{key.lower()}")']  # noqa
                if 'link' in option:
                    screen_constant = f"{option['link'].upper()}_SCREEN"
                    lpad = " " * 16
                    screen_case_lines += [fr'{lpad}navigate_to ${screen_constant}; return 0;;']  # noqa
                elif 'action' in option:
                    lpad = " " * 16
                    screen_case_lines += [fr'{lpad}INVOKE_ON_EXIT="{option["action"]}"; return 1;;']  # noqa

            screen_case_lines += [
                r'        esac',
                ''
            ]

            if i == (len(self.screens) - 1):
                screen_case_lines += [
                    '    fi',
                    ''
                ]

        check_keystroke_lines += screen_case_lines

        check_keystroke_lines += self.get_comment_lines([
            "Handle [ESC] key and left arrow.",
            "[unix.stackexchange.com/a/179193]"
        ], 4)
        check_keystroke_lines += [
            r'    case "$key" in',
            r"        $'\x1b')  # Handle ESC sequence.",
            r'            read -rsn1 -t 0.1 additional_bytes',
            r'            if [[ "$additional_bytes" == "[" ]]; then',
            r'                read -rsn1 -t 0.1 additional_bytes',
            r'                case "$additional_bytes" in',
            r'                    "D")  # Left arrow.',
            r'                        navigate_back; return 0;;',
            r'                    *)  # Other escape sequences.',
            r'                        return 0;;',
            r'                esac',
            r'            fi;;',
            r'        *)  # Other single byte (char) cases.',
            r'            return 0;;',
            r'    esac',
            r''
        ]

        check_keystroke_lines += self.get_comment_lines("Default fallthrough.", 4)  # noqa
        check_keystroke_lines += [
            '    return 1',
            '}'
        ]

        return check_keystroke_lines

    def get_screen_flow_code(self) -> str:
        screen_flow_code = [self.get_section_title('Screen flow')]
        screen_flow_code += [""]
        screen_flow_code += self.get_screen_flow_state_variables_lines()
        screen_flow_code += [""]
        screen_flow_code += self.get_screen_flow_constants_lines()
        screen_flow_code += [""]
        screen_flow_code += self.get_navigate_to_method_lines()
        screen_flow_code += [""]
        screen_flow_code += self.get_navigate_back_method_lines()
        screen_flow_code += [""]
        screen_flow_code += self.get_show_active_screen_method_lines()
        screen_flow_code += [""]
        screen_flow_code += self.get_check_keystroke_method_lines()
        screen_flow_code += ["\n\n"]

        return '\n'.join(screen_flow_code)

#   Screen rendering ───────────────────────────────────────────────────────────

    def get_invoke_action_on_exit_lines(self) -> List[str]:
        return [
            'invoke_action_on_exit() {',
            '    clear_screen',
            '    eval $INVOKE_ON_EXIT',
            '}'
        ]

    def get_show_exit_screen_lines(self) -> List[str]:
        return [
            r'show_exit_screen() {',
            r'    clear_screen',
            r'    printf "Exited \n\n"',
            r'}'
        ]

    def get_screen_rendering_code(self) -> str:
        screen_rendering_code = [self.get_section_title('Screen rendering')]
        screen_rendering_code += [""]
        screen_rendering_code += self.get_invoke_action_on_exit_lines()
        screen_rendering_code += [""]
        screen_rendering_code += self.get_show_exit_screen_lines()
        screen_rendering_code += ["\n\n"]

        return '\n'.join(screen_rendering_code)

#   Nacar app's main loop ──────────────────────────────────────────────────────

    def get_main_loop_code(self) -> str:
        main_loop_lines = [
            self.get_section_title('Main loop'),
            "",
            r'''# Capture Ctrl+C interrupts.''',
            # [kb.mit.edu/confluence/pages/viewpage.action?pageId=3907156]
            r'''trap '{ exit_screen; exit 1; }' INT''',
            "",
            r'''navigate_to $HOME_SCREEN''',
            "",
            r'''while :; do''',
            r'''    show_active_screen || break;''',
            r'''done''',
            "",
            r'''if [[ -n $INVOKE_ON_EXIT ]]; then''',
            r'''    invoke_action_on_exit''',
            r'''else''',
            r'''    show_exit_screen''',
            r'''fi''',
            ""
        ]

        return '\n'.join(main_loop_lines)

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
        bash_translation += self.get_screen_building_utilities()
        bash_translation += self.get_screen_flow_code()
        bash_translation += self.get_screen_rendering_code()
        bash_translation += self.get_main_loop_code()

        return bash_translation
