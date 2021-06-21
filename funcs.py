
# hierarchical struct -> help supercedes func
def fn(args: dict) -> str:
    if args['help'] == True:
        return 'help'
    else:
        return args['func']

def passesDirCheck(args: dict) -> bool:
    from os import path
    from utils import drawCodes
    if path.isdir(args['conf']):
        return True
    else:
        print(drawCodes('tumbo') + '\n')
        print("the config path in `tumbo.py` doesn't seem to exist")
        print(f"offending path: '{args['conf']}'")


class _internals:
    def TypeSearch(args: dict, match: str) -> list:
        from os import listdir
        return [f for f in listdir(args['conf']) if match in f]


def helpFunc(args: dict) -> None:
    from helps import Helper
    if len(args['func']) > 1:
        Helper(args['func'], args)
    else:
        Helper('*', args)

def newFunc(args: dict) -> None:
    from os import listdir
    from utils import drawCodes
    from pathlib import Path
    print('pop')

def lsFunc(args: dict) -> None:
    from os import listdir
    if 'list' in args.keys():
        if args['list'] == '/\\': # 'type' argument
            [print(i) for i in listdir(args['conf'])]

        else:
            ls = _internals.TypeSearch(args, args['list'])
            if len(ls) > 0:
                for i in ls:
                        print(f"   '{args['list']}' found in '{i}'")
                        if input(f"   list contents of '{i}'? (ENTER for yes) ") == "":
                            print("\n" + open((args['conf'] + '/' + i), 'r').read())
            else:
                print(" no matching types found for '%s'" % args['list'])

    else:
        [print(i) for i in listdir(args['conf'])]
            


def evalArgs(args: dict):
    if passesDirCheck(args):
        do = {
            'help': helpFunc,
            'new': newFunc,
            'list': lsFunc,
            'search': helpFunc,
            'update': helpFunc,
            'remove': helpFunc,
            'source': helpFunc,
        }
        do[fn(args)](args)