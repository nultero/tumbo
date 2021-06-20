
# hierarchical struct -> help supercedes func
def fn(args: dict) -> str:
    if args['help']:
        return 'help'
    else:
        return args['func']
    
def helpFunc(args: dict) -> None:
    from helps import Helper
    if len(args['func']) > 1:
        Helper(args['func'])
    else:
        Helper('*')

def newFunc(args: dict) -> None:
    from os import path
    from utils import drawCodes
    from pathlib import Path

    if path.isdir(args['conf']):
        # pth = Path()
        # with open(args['conf'], 'r') as f:
        #     conf = f.read()
        # unfinished
        print(args['conf'])

    else:
        print(drawCodes('tumbo') + '\n')
        print("the config path in `tumbo.py` doesn't seem to exist")

def evalArgs(args: dict):
    do = {
        'help': helpFunc,
        'new': newFunc,
        'list': helpFunc,
        'search': helpFunc,
        'update': helpFunc,
        'remove': helpFunc,
        'source': helpFunc,
    }
    do[fn(args)](args)