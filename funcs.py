from logicClass import Logic as Lg


def helpFunc(args: dict) -> None:
    from helps import Helper

    if len(args["func"]) > 1:
        Helper(args["func"], args)
    else:
        Helper("*", args)



def sourceFunc(args: dict) -> None:
    import json

    types = Lg.Types(args["conf"])
    aliases = ""

    for k, val in types.items():
        typeName = args["conf"] + "/" + val

        with open(typeName, "r") as dataFile:
            typedAliases = json.load(dataFile)
        
            aliases += f"#####>  {val}  <##### \n"
            for short, contents in typedAliases.items():
                aliases += Lg.AliasString(short, contents) + "\n"

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
    
    for ty in Lg.Types(args["conf"]).values():
        d = Lg.Aliases(args["conf"] + "/" + ty)

        for key, val in d.items(): # tack on a thing to tell where it came from
            d[key] = val + "#####" + ty

        tumbo.update(d)

    while tumbo:
        cut = []
        for k, v in tumbo.items():
            if srch not in k and srch not in v:
                cut.append(k)

        [tumbo.pop(k) for k in cut]
        print(">"*5)
        if len(tumbo) == 1:
            for k, v in tumbo.items():
                chunks = v.split("#####")
                v = chunks[0]
                aliasType = chunks[1]

                print(f" >> found in type : '{aliasType}'")
                s = f" >> {Lg.AliasString(k, v)}"
                print("  -" * int(len(s)/3) + "\n" + s)
                quit()

        elif len(tumbo) == 0:
            print("no results found")
            quit()

        [print(Lg.AliasString(k, v.split("####")[0])) for k,v in tumbo.items()]
        print("<"*5)
        srch = input("\nnew string to cut down results? (ENTER to quit) : ")
        if len(srch) == 0:
            quit()
    


def newFunc(args: dict) -> None:
    args = Lg.CheckSecondaryArg(args, "new")
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

        f = Lg.InputInTypes(args["conf"], inputStr="\ntype to define new alias under? ")
        
        import json

        aliases = Lg.Aliases(f)
        new = input(" new alias' shorthand: ")
        content = input(" new alias' commands: ")
        aliases[new] = content
        with open(f, "w") as out:
            json.dump(aliases, out)
        print("> done!")



def lsFunc(args: dict) -> None:

    if "list" in args.keys():  # NOT the argument -- "list" should be paired to alias or type
        if args["list"] == "/\\":  # 'type' argument
            Lg.PrintTypes(args["conf"])

        else:
            ls = Lg.TypeSearch(args["conf"], args["list"])
            if len(ls) > 0:
                for i in ls:
                    print(f"   '{args['list']}' found in '{i}'")
                    _ = f"   list contents of '{i}'? (ENTER for yes) "
                    if input(_) == "":
                        pth = args["conf"] + "/" + i
                        Lg.PrintAliases(pth, len(_))

            else:
                print(" no matching types found for '%s'" % args["list"])

    else:
        ty = Lg.Types(args["conf"])
        keys = sorted([ty[i] for i in ty])

        for i in keys:
            print(f"|>  {i}")
            pth = args["conf"] + "/" + i
            Lg.ListAliases(pth, 1)
            print("")
        



# 'update' and 'remove' context methods
def _grabType(conf: str, inputProxy: str) -> str:
    f = Lg.InputInTypes(conf, inputStr=inputProxy)
    return f

def _grabContext(args: dict, funcName: str):
    args = Lg.CheckSecondaryArg(args, funcName)
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
        if Lg.ConfirmChanges():
            from os import remove
            remove(f)
            print(f"done! removed -> '{f}'")

    elif args["secondary"] == "alias":
        key = Lg.GetAlias(f, "remove")
        aliases = Lg.Aliases(f)
        print("\n->   STAGING   <-")
        print(f"REMOVING   '{key}'")
        print(f"FROM       '{f}'")
        if Lg.ConfirmChanges():
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
        key = Lg.GetAlias(f, "update")
        aliases = Lg.Aliases(f)

        print(f"\n>---- current alias shorthand is '{key}'")
        newAlias = input("updated alias' shorthand? (ENTER to keep current) : ")
        if newAlias == "":
            newAlias = key

        print(f"\n>---- current alias content is '{aliases[key]}'")
        newContent = input("updated alias' content? (ENTER to keep current) : ")
        if newContent == "":
            newContent = aliases[key]

        print("\n->   STAGING   <-")
        print(f"CHANGING   '{Lg.AliasString(key, aliases[key])}'")
        print(f"TO         '{Lg.AliasString(newAlias, newContent)}'")

        if Lg.ConfirmChanges():
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
