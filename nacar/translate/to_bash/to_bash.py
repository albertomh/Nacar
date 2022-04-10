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

#   Screen flow ────────────────────────────────────────────────────────────────

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
