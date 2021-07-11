#!/bin/python3

from sys import argv
from utils import drawCodes
from parser import parse
from funcs import evalArgs
import pathlib

DEFAULT_CONFIG_DIR_PATH = (
    "/home/nultero/.nultero/tumbo"  # main path Tumbo sends aliases to
)
DEFAULT_SHELL_SOURCE_PATH = (
    "/home/nultero/.bash_aliases"  # .bash_aliases, .zsh_aliases, a .rc, etc.
)
TRUNCATE_SOURCE = True  # set to false to have Tumbo append to $SOURCE instead
# NB: file truncation only triggers when SOURCE is used as an argument


def isConfigEmpty(args: dict) -> bool:
    return not len(args["conf"]) * len(args["source"])


def main():

    if len(argv) > 1:

        args = {}
        args["conf"] = DEFAULT_CONFIG_DIR_PATH
        args["source"] = DEFAULT_SHELL_SOURCE_PATH
        args["trunc"] = TRUNCATE_SOURCE

        if not isConfigEmpty(args):
            args.update(parse(argv[1:]))
            evalArgs(args)

        else:
            print(drawCodes("tumbo"))
            print(f"\n\n 'tumbo.py' has empty config paths -- pls fix")

    else:
        print(f"{drawCodes('tumboNoArgs')}")
        print("  (run '-h' or '--help' to see opts)")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n>>> qq")
