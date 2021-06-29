#####<<internals>>########
class _I:

    """Extra reusables for the functions to borrow in logic."""

    def AliasString(short: str, contents: str) -> str:
        return f'alias {short}="{contents}"'

    def PrintTypes(conf: str) -> None:
        from os import listdir

        [print(f"|>  {i}") for i in sorted(listdir(conf))]

    def Aliases(conf: str) -> dict:
        import json

        with open(conf, "r") as f:
            return json.load(f)

    def PrintAliases(conf: str, numDashes: int) -> None:
        d = _I.Aliases(conf)

        print("-" * numDashes)
        for k, v in d.items():
            print(_I.AliasString(k, v))

    def NumberedAliases(conf: str) -> list:
        d = _I.Aliases(conf)
        for i, vals in enumerate(sorted(d.items())):
            print(f"{i+1}.   {_I.AliasString(vals[0], vals[1])}")
        return [k for k in sorted(d.keys())]

    def GetAlias(conf: str, action: str) -> str:
        aliases = _I.NumberedAliases(conf)
        i = int(input("\nwhich alias to " + action + "? ")) - 1
        for n, al in enumerate(aliases):
            if n == i:
                return aliases[i]

        print(f"'{i+1}' is not an option in the aliases above")

    def TypeSearch(conf: str, match: str) -> list:
        from os import listdir
        return sorted([f for f in listdir(conf) if match in f])

    def Types(conf: str) -> dict:
        from os import listdir
        return {i: f for i, f in sorted(enumerate(listdir(conf)))}

    def InputInTypes(conf: str, inputStr: str) -> str:
        tmp = f"\n/// defined types in: {conf} \\\\\\"
        print(tmp + "\n" + "-" * len(tmp))
        aliasTypes = _I.Types(conf)

        if len(aliasTypes) < 1:
            from utils import drawCodes
            print(drawCodes("tumbo") + "\n\n")
            print("|>  there are no defined types available")
            print("|>  try running 'tumbo new type'")
            quit()

        [print(f" {i+1}. {f}") for i, f in aliasTypes.items()]
        try:
            i = int(input(inputStr)) - 1
            if i in aliasTypes.keys():
                return conf + "/" + aliasTypes[i]

            print(f"\n '{i+1}' not in the types above")
            quit()
        except Exception:
            print("!! some input's gone wrong")

    def NotFound(opt: str, funcName: str) -> None:
        print(
            f"'{opt}' not a valid opt for {funcName.upper()} and is not in ALIAS or TYPE"
        )
        quit()

    def IsInSecondaries(opt: str, funcName: str) -> str:
        sc = ["alias", "type"]
        if len(opt) == 0:
            quit()
        for i in sc:
            if opt in i:
                return i

        _I.NotFound(opt, funcName)

    def CheckSecondaryArg(args: dict, funcName: str) -> dict:
        if "secondary" not in args.keys():
            print(f" '{funcName.upper()}' takes an argument, ALIAS or TYPE")
            opt = input(
                " input any letter of either as choice, or ENTER to exit: "
            ).lower()

            args["secondary"] = _I.IsInSecondaries(opt, funcName)

        return args

    def ConfirmChanges() -> bool:
        choice = input(f"CONFIRM change? [ y / n ] : ")
        while choice != "y" and choice != "n":
            print("\n --->  Invalid input.")
            choice = input(f"CONFIRM change? [ y / n ] : ")
        return True if choice == "y" else False

#####<<internals />>########


# # # # # # # # # # # # # # #
#  FUNCS
#
def helpFunc(args: dict) -> None:
    from helps import Helper

    if len(args["func"]) > 1:
        Helper(args["func"], args)
    else:
        Helper("*", args)



def sourceFunc(args: dict) -> None:
    import json

    types = _I.Types(args["conf"])
    aliases = ""

    for key, val in types.items():
        typeName = args["conf"] + "/" + val

        with open(typeName, "r") as dataFile:
            typedAliases = json.load(dataFile)
        
            aliases += f"#####>  {val}  <##### \n"
            for short, contents in typedAliases.items():
                aliases += _I.AliasString(short, contents) + "\n"

            aliases += "\n" * 2

    trunc = "w" if args["trunc"] else "a"

    with open(args["source"], trunc) as f:
        f.write(aliases)
    
    from utils import drawCodes
    print(drawCodes("tumboHat"))



def searchFunc(args: dict) -> None:

    if "search" not in args.keys():
        args["search"] = input("> search for? ")
    
    srch = args["search"]
    tumbo = {}
    
    for ty in _I.Types(args["conf"]).values():
        tumbo.update(_I.Aliases(
            args["conf"] + "/" + ty
        ))

    while tumbo:
        cut = []
        for k, v in tumbo.items():
            if srch not in k and srch not in v:
                cut.append(k)

        [tumbo.pop(k) for k in cut]
        print(">"*5)
        if len(tumbo) == 1:
            [print(" >> " + _I.AliasString(k, v)) for k,v in tumbo.items()]
            quit()

        elif len(tumbo) == 0:
            print("no results found")
            quit()

        [print(_I.AliasString(k, v)) for k,v in tumbo.items()]
        print("<"*5)
        srch = input("\nnew string to cut down results? (ENTER to quit) : ")
        if len(srch) == 0:
            quit()
    


def newFunc(args: dict) -> None:
    args = _I.CheckSecondaryArg(args, "new")
    if args["secondary"] == "type":
        ty = input("new alias TYPE name: ")
        loc = args["conf"] + "/" + ty
        try:
            with open(loc, "w") as f:
                import json
                d = {}
                json.dump(d, f)
                print("created type: '" + ty + "' in " + loc)

        except FileExistsError:
            print("!! problem creating new type:")
            print(f"type '{ty}' already exists as file in {args['conf']}")

    elif args["secondary"] == "alias":
        f = _I.InputInTypes(args["conf"], inputStr="\ntype to define new alias under? ")
        import json

        aliases = _I.Aliases(f)
        new = input(" new alias' shorthand: ")
        content = input(" new alias' commands: ")
        aliases[new] = content
        with open(f, "w") as out:
            json.dump(aliases, out)
        print("> done!")



def lsFunc(args: dict) -> None:

    # should dump all by default

    if "list" in args.keys():  # NOT the argument -- "list" should be paired to alias or type
        if args["list"] == "/\\":  # 'type' argument
            _I.PrintTypes(args["conf"])

        else:
            ls = _I.TypeSearch(args["conf"], args["list"])
            if len(ls) > 0:
                for i in ls:
                    print(f"   '{args['list']}' found in '{i}'")
                    _ = f"   list contents of '{i}'? (ENTER for yes) "
                    if input(_) == "":
                        pth = args["conf"] + "/" + i
                        _I.PrintAliases(pth, len(_))

            else:
                print(" no matching types found for '%s'" % args["list"])

    else:
        _I.PrintTypes(args["conf"])



# 'update' and 'remove' context methods
def _grabType(conf: str, inputProxy: str) -> str:
    f = _I.InputInTypes(conf, inputStr=inputProxy)
    print(f"(chosen type: '{f.split('/')[-1]}')\n")
    return f

def _grabContext(args: dict, funcName: str):
    args = _I.CheckSecondaryArg(args, funcName)
    if args["secondary"] == "type":
        inputProx = "type to rename? " if funcName == "update" else "type to remove? "
        f = _grabType(args["conf"], inputProxy=("\n" + inputProx))

    elif args["secondary"] == "alias":
        inputProx = "type alias is under? " if funcName == "update" else "type alias to remove is under? "
        f = _grabType(args["conf"], inputProxy=("\n" + inputProx))

    return [args, f]



def removeFunc(args: dict) -> None:

    ls = _grabContext(args, funcName="remove")
    args = ls[0]
    f = ls[1]

    if args["secondary"] == "type":
        print("\n->   STAGING   <-")
        print(f"REMOVING   '{f}'")
        if _I.ConfirmChanges():
            from os import remove
            remove(f)
            print(f"done! removed -> '{f}'")

    elif args["secondary"] == "alias":
        key = _I.GetAlias(f, "remove")
        aliases = _I.Aliases(f)
        print("\n->   STAGING   <-")
        print(f"REMOVING   '{key}'")
        print(f"FROM       '{f}'")
        if _I.ConfirmChanges():
            import json
            aliases.pop(key)
            print(f"> removed -> {key}")
            with open(f, "w") as fl:
                json.dump(aliases, fl)
            print(f"> done!")



def updateFunc(args: dict) -> None:
    ls = _grabContext(args, funcName="update")
    args = ls[0]
    f = ls[1]

    if args["secondary"] == "type":
        newName = input("\nnew name for this renamed type? ")
        from os import rename
        newPath = args["conf"] + "/" + newName
        rename(f, newPath)
        print("> done!")

    elif args["secondary"] == "alias":
        key = _I.GetAlias(f, "update")
        aliases = _I.Aliases(f)

        print(f"\n>---- current alias shorthand is '{key}'")
        newAlias = input("updated alias' shorthand? (ENTER to keep current) : ")
        if newAlias == "":
            newAlias = key

        print(f"\n>---- current alias content is '{aliases[key]}'")
        newContent = input("updated alias' content? (ENTER to keep current) : ")
        if newContent == "":
            newContent = aliases[key]

        print("\n->   STAGING   <-")
        print(f"CHANGING   '{_I.AliasString(key, aliases[key])}'")
        print(f"TO         '{_I.AliasString(newAlias, newContent)}'")

        if _I.ConfirmChanges():
            aliases.pop(key)
            aliases[newAlias] = newContent
            import json
            with open(f, "w") as fl:
                json.dump(aliases, fl)
            print("> done!")



def passesDirCheck(args: dict) -> bool:
    from os import path
    from utils import drawCodes

    if path.isdir(args["conf"]):
        return True

    else:
        print(drawCodes("tumbo") + "\n")
        print("the config path in `tumbo.py` doesn't seem to exist")
        print(f"offending path: '{args['conf']}'")


def evalArgs(args: dict):  # the actual calls

    # hierarchical struct -> help flag supercedes func
    def _fn(args: dict) -> str:
        return "help" if args["help"] else args["func"]

    if passesDirCheck(args):
        do = {
            "help": helpFunc,
            "new": newFunc,
            "list": lsFunc,
            "search": searchFunc,
            "update": updateFunc,
            "remove": removeFunc,
            "source": sourceFunc,
        }
        do[_fn(args)](args)
