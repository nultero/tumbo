class Logic:

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


    def ListAliases(conf: str, tabs: int) -> None:
        d = Logic.Aliases(conf)

        for k, v in sorted(d.items()):
            print(
                "\t" * tabs + 
                    Logic.AliasString(k, v)
                )


    def PrintAliases(conf: str, numDashes: int) -> None:
        d = Logic.Aliases(conf)

        print("-" * numDashes)
        for k, v in d.items():
            print(Logic.AliasString(k, v))


    def ShowNumberedAliases(aliases: dict) -> None:
        for i, vals in enumerate(sorted(aliases.items())):
            print(f"{i+1}.   {Logic.AliasString(vals[0], vals[1])}")


    def GetAlias(conf: str, action: str) -> str:

        aliases = Logic.Aliases(conf)

        while aliases:
            Logic.ShowNumberedAliases(aliases)
            i = input("\nwhich alias to " + action + "? ")

            if not i.isalpha():
                i = int(i) - 1
                for n, al in enumerate(sorted(aliases.keys())):
                    if n == i:
                        return al

                print(f"'{i+1}' is not an option in the aliases above"); quit()
            
            else:
                aliases = {k:v for k,v in aliases.items() if i in k}
            
            if len(aliases) == 1:
                for k, v in aliases.items():
                    return k



    def TypeSearch(conf: str, match: str) -> list:
        from os import listdir
        return sorted([f for f in listdir(conf) if match in f])


    def Types(conf: str) -> dict:
        from os import listdir
        return {i: f for i, f in enumerate(listdir(conf))}


    def InputInTypes(conf: str, inputStr: str) -> str:
        tmp = f"\n/// defined types in: {conf} \\\\\\"
        print(tmp + "\n" + "-" * len(tmp))

        aliasTypes = Logic.Types(conf)

        if len(aliasTypes) < 1:
            from utils import drawCodes
            print(drawCodes("tumbo") + "\n\n")
            print("|>  there are no defined types available")
            print("|>  try running 'tumbo new type'")
            quit()


        while aliasTypes.items():

            [print(f" {i+1}. {f}") for i, f in aliasTypes.items()]

            inp = input(inputStr)

            if len(inp) == 0:
                print("\n>>> qq"); quit()

            if not inp.isalpha():
                try: 
                    i = int(inp) - 1
                    if i in aliasTypes.keys():
                        print(f">>> '{aliasTypes[i]}' selected")
                        return conf + "/" + aliasTypes[i]

                    else:
                        print(f"|>  '{i+1}': input out of bounds"); quit()

                except Exception: 
                    print("|>  tumbo treated this input as a number, " +
                            "so it's probably out of bounds somewhere"); quit()

            cut = []
            for ty in aliasTypes.values():
                if inp in ty:
                    cut.append(ty)

            aliasTypes = {i: f for i, f in enumerate(cut)}
            if len(aliasTypes) == 1:
                print(f">>> '{aliasTypes[0]}' selected")
                return conf + "/" + aliasTypes[0]
    

        print(f"\n '{inp}' not in the types above")
        quit()



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

        Logic.NotFound(opt, funcName)


    def CheckSecondaryArg(args: dict, funcName: str) -> dict:
        if "secondary" not in args.keys():
            print(f" '{funcName.upper()}' takes an argument, ALIAS or TYPE")
            opt = input(
                " input any letter of either as choice, or ENTER to exit: "
            ).lower()

            args["secondary"] = Logic.IsInSecondaries(opt, funcName)

        return args


    def ConfirmChanges() -> bool:
        choice = input(f"CONFIRM change? [ y / n ] : ")
        while choice != "y" and choice != "n":
            print("\n --->  Invalid input.")
            choice = input(f"CONFIRM change? [ y / n ] : ")
        return True if choice == "y" else False