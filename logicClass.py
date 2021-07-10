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

    def NumberedAliases(conf: str) -> list:
        d = Logic.Aliases(conf)
        for i, vals in enumerate(sorted(d.items())):
            print(f"{i+1}.   {Logic.AliasString(vals[0], vals[1])}")
        return [k for k in sorted(d.keys())]

    def GetAlias(conf: str, action: str) -> str:
        aliases = Logic.NumberedAliases(conf)
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