
# hierarchical struct -> help supercedes func
def fn(args: dict) -> str:
    return 'help' if args['help'] else args['func']

def passesDirCheck(args: dict) -> bool:
    from os import path
    from utils import drawCodes
    if path.isdir(args['conf']):
        return True
    else:
        print(drawCodes('tumbo') + '\n')
        print("the config path in `tumbo.py` doesn't seem to exist")
        print(f"offending path: '{args['conf']}'")

#####<<internals>>########
class _internals:
    def PrintTypes(conf: str):
        from os import listdir
        [print(i) for i in sorted(listdir(conf))]

    def TypeSearch(args: dict, match: str) -> list:
        from os import listdir
        return sorted([f for f in listdir(args['conf']) if match in f])

    def Types(args: dict) -> dict:
        from os import listdir
        return {i:f for i,f in sorted(enumerate(listdir(args['conf'])))}


    def NotFound(opt: str, func: str) -> None:
        print(f"'{opt}' not a valid opt for {func.upper()} and is not in ALIAS or TYPE")
        quit()

    def IsInSecondaries(opt: str, func: str) -> str:
        sc = ['alias', 'type']
        if len(opt) == 0: quit()
        for i in sc:
            if opt in i:
                return i

        _internals.NotFound(opt, func)
#####<<internals />>########


#  FUNCS
def helpFunc(args: dict) -> None:
    from helps import Helper
    if len(args['func']) > 1:
        Helper(args['func'], args)
    else:
        Helper('*', args)



def newFunc(args: dict) -> None:

    def _new(rg: str, args: dict):
        fn = _internals.IsInSecondaries(rg, 'new')
        if fn == 'type':
            ty = input("new type name: ")
            loc = args['conf'] + '/' + ty
            try: 
                with open(loc, "w") as f: 
                    import json
                    d = {}
                    json.dump(d, f)

            except FileExistsError: 
                print("!! problem creating new type:")
                print(f"type '{ty}' already exists as file in {args['conf']}")
    
        else: 
            tmp = f"\n/// defined types in: {args['conf']} \\\\\\"
            print(tmp + '\n' + '-' * len(tmp))
            aliasTypes = _internals.Types(args)
            for i,f in aliasTypes.items():
                print(f" {i+1}. {f}")
            try:
                inp = int(input("\ntype to define new alias under? ")) - 1
                if inp in aliasTypes.keys():
                    import json
                    pth = args['conf'] + '/' + aliasTypes[inp]
                    with open(pth, 'r') as f:
                        aliases = json.loads(f.read())
                    new = input(" new alias' shorthand: ")
                    cont = input(" new alias' commands: ")
                    aliases[new] = cont
                    with open(pth, 'w') as f:
                        json.dump(aliases, f)
                    print("> done!")

            except Exception:
                print("!! some input's gone wrong")


    if 'secondary' not in args.keys():
        print(" 'new' takes an argument, ALIAS or TYPE")
        opt = input(" input any letter of either as choice, or ENTER to exit: ").lower()
        _new(opt, args)

    elif 'secondary' in args.keys():
        _new(args['secondary'], args)



def lsFunc(args: dict) -> None:

    if 'list' in args.keys():
        if args['list'] == '/\\': # 'type' argument
            _internals.PrintTypes(args['conf'])

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
        _internals.PrintTypes(args['conf'])
            


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