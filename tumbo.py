#!/bin/python3

from sys import argv
from utils import drawCodes
from parser import parse
from funcs import evalArgs
from os import path

DEFAULT_CONFIG_DIR_PATH = ''  # main path Tumbo sends aliases to
DEFAULT_SHELL_SOURCE_PATH = '' # .bash_aliases, .zsh_aliases, a .rc, etc.
TRUNCATE_SOURCE = True    # set to false to have Tumbo append to $SOURCE instead
# NB: file truncation only triggers when SOURCE is used as an argument

def isConfigEmpty(rgs: dict) -> bool:
    return not len(rgs['conf']) * len(rgs['source'])

def main():    

    if len(argv) > 1:

        rgs = {}
        rgs['conf'] = DEFAULT_CONFIG_DIR_PATH
        rgs['source'] = DEFAULT_SHELL_SOURCE_PATH
        rgs['trunc'] = TRUNCATE_SOURCE

        if not isConfigEmpty(rgs):
            rgs.update(parse(argv[1:]))
            print(rgs)
            evalArgs(rgs)

        else:
            print(drawCodes('tumbo'))
            print(f"\n\n 'tumbo.py' has empty config paths -- pls fix")

    else:
        print(f"{drawCodes('tumboNoArgs')}")
        print("  (run '-h' or '--help' to see opts)")

if __name__ == '__main__':
    main()