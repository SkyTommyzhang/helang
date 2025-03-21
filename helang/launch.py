import sys
import traceback

from typing import Dict
from helang.lexer import Lexer
from helang.parser import Parser
from helang.exceptions import HeLangException
from helang.u8 import U8


SHELL_HELP = """
.help  Print this help message
.exit  Exit the shell
.env   Print current environments
""".strip()


def process_shell_keywords(text: str, env: Dict[str, U8]):
    if text == 'help':
        print(SHELL_HELP)
    elif text == 'exit':
        print('Saint He bless you.')
        sys.exit(0)
    elif text == 'env':
        for k, v in env.items():
            print(f'{k}: {v}')
    else:
        print(f'Invalid shell keyword: {text}')


def launch_shell():
    env = dict()
    while True:
        text = input('Speak to Saint He > ').strip()
        if text == '':
            continue

        if text.startswith('.'):
            process_shell_keywords(text[1:], env)
            continue

        if not text.endswith(';'):
            text += ';'
        lexer = Lexer(text)
        parser = Parser(lexer.lex())
        try:
            parser.parse().evaluate(env)
        except HeLangException:
            traceback.print_exc()
        except Exception as e:
            print('Fatal Error! Revise Saint He\'s videos!')
            raise e


def launch_great_script():
    with open('./great.he', 'r') as f:
        content = f.read()
    lexer = Lexer(content)
    parser = Parser(lexer.lex())
    env = dict()
    parser.parse().evaluate(env)


LAUNCHERS = {
    'great': launch_great_script,
    'shell': launch_shell,
}


def main():
    """
    Main function
    """
    target = sys.argv[-1]
    if target not in LAUNCHERS.keys():
        legal_targets = ', '.join(LAUNCHERS.keys())
        print(f'Invalid launch target {target}, expected target: {legal_targets}.')
        sys.exit(-1)

    LAUNCHERS[target]()


if __name__ == '__main__':
    main()
