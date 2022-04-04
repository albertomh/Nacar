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
    [I] template_data: dict
    [I] set_template_data(data: dict) -> None
    [I] screens: List[str]
    [I] set_screens() -> None
    [I] __init__(blueprint: dict) -> None

    Bash translator utilities
      ├ [I] get_target_language() -> TargetLanguage
      ├ [I] get_max_line_length() -> str
      ├ [I] get_comment_lines(content: str) -> List[str]
      └ [I] get_section_title(title: str) -> str

    File heading
      └ [I] set_heading_template_variables() -> None
    """

    template_data = {}

    def set_template_data(self, data: dict) -> None:
        self.template_data = data

    screens: List[str] = []

    def set_screens(self) -> None:
        self.screens = Schema.get_screen_names(self.blueprint)

    def __init__(self, blueprint: dict) -> None:
        translator_dir = dirname(abspath(__file__))
        super().__init__(blueprint, translator_dir)

#   Bash translator utilities ──────────────────────────────────────────────────

    @staticmethod
    def get_target_language() -> TargetLanguage:
        return TargetLanguage.BASH

    def get_max_line_length(self):
        return 80

#   File heading ───────────────────────────────────────────────────────────────

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

#   Nacar app config ───────────────────────────────────────────────────────────

    def set_app_config_template_variables(self) -> None:
        app_config_data = {
            'screen_width': self.blueprint['meta']['width'],
            'title': self.blueprint['title']
        }
        self.set_template_data({
            **self.template_data,
            **{'app_config': app_config_data}
        })

#   Utilities ──────────────────────────────────────────────────────────────────

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
            options = Schema.get_options_for_screen(self.blueprint, screen)
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

    def get_show_screen_methods_lines(self) -> List[str]:
        screen_methods_lines = []

        for screen in self.screens:
            screen_methods_lines += [
                f'show_{screen.lower()}_screen() {{',
                '    print_screen_top',
            ]

            options = Schema.get_options_for_screen(self.blueprint, screen)
            for option in options:
                name: str = option['name']
                printf_snippet = r'    printf "\U2502 '
                key_snippet = fr'[${{YEL}}{name[0].upper()}${{END}}]'
                len_right = self.blueprint['meta']['width'] - (len(name) + 7)
                right_snippet = fr'%{len_right}s \U2502\n"'
                screen_methods_lines += [
                    fr'{printf_snippet}{key_snippet}{name.lower()[1:]} {right_snippet}'  # noqa
                ]

            max_options = Schema.get_max_screen_options_in_blueprint(self.blueprint)  # noqa
            bottom_padding = 1 + (max_options - len(options))

            screen_methods_lines += [
                f'    print_screen_bottom {bottom_padding}',
                '',
                f'    check_keystroke ${screen.upper()}_SCREEN',
                '}'
            ]

        return screen_methods_lines

    def get_invoke_action_on_exit_lines(self) -> List[str]:
        return [
            'invoke_action_on_exit() {',
            '    clear_screen',
            '    eval $INVOKE_ON_EXIT',
            '}'
        ]

    def get_show_exit_screen_lines(self) -> List[str]:
        show_exit_lines = [
            r'show_exit_screen() {',
            r'    clear_screen'
        ]
        if self.blueprint['meta']['show_made_with_on_exit']:
            show_exit_lines += [r'    printf "Exited \U1F41A Made with Nacar \n\n"']  # noqa
        else:
            show_exit_lines += [r'    printf "Exited \n\n"']
        show_exit_lines += [
            r'}'
        ]
        return show_exit_lines

    def get_screen_rendering_code(self) -> str:
        screen_rendering_code = [self.get_section_title('Screen rendering')]
        screen_rendering_code += [""]
        screen_rendering_code += self.get_show_screen_methods_lines()
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

        self.set_heading_template_variables()
        self.set_app_config_template_variables()
        self.set_utilities_template_variables()

        template = self.jinja_env.get_template('base.sh.template')
        bash_translation: str = template.render(self.template_data)

        return bash_translation
