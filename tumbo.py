#!/bin/python3

from sys import argv
from utils import drawCodes
from parser import parse
from funcs import evalArgs

DEFAULT_CONFIG_PATH = ''  # main path Tumbo sends aliases to
DEFAULT_SHELL_SOURCE = '' # .bash_aliases, .zsh_aliases, a .rc, etc.
TRUNCATE_SOURCE = True    # set to false to have Tumbo append to $SOURCE instead
# NB: file truncation only triggers when SOURCE is used as an argument

def main():    

    if len(argv) > 1:

        rgs = {}
        rgs['conf'] = DEFAULT_CONFIG_PATH
        rgs['source'] = DEFAULT_SHELL_SOURCE
        rgs['trunc'] = TRUNCATE_SOURCE

        # still need to check if the configs are empty on run

        rgs.update(parse(argv[1:]))
        print(rgs)
        evalArgs(rgs)

    else:
        print(f"{drawCodes('tumboNoArgs')}")
        print("  (run '-h' or '--help' to see opts)")

if __name__ == '__main__':
    main()