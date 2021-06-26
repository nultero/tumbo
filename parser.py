def parse(args: list) -> dict:

    from typing import Counter
    from utils import throwInvalid

    argsMap = {"func": "", "help": False}
    validSet = ["new", "list", "search", "update", "remove", "source"]
    secondaryArgs = ["alias", "type"]

    def isHelp(arg: str) -> bool:
        if arg == "-h":
            return True
        flagCounts = Counter(arg.replace("-", ""))
        return True if (flagCounts["help"]) != 0 else False

    def printBar(tmp: str, cur: str) -> None:
        print(tmp)
        print("-" * len(tmp))

    # reduce args into dict to eval
    # queue based, so 'help' order is irrelevant
    while args:
        cur = args[0]

        if isHelp(cur):
            argsMap["help"] = True

        elif cur in validSet:
            if len(argsMap["func"]) < 1:
                argsMap["func"] = cur
            else:
                throwInvalid(2, "")

        elif cur not in validSet:

            # there is a valid arg already
            if len(argsMap["func"]) > 1:

                if argsMap["func"] == "source":
                    throwInvalid(3, cur)

                elif argsMap["func"] != "search" and argsMap["func"] != "list":
                    if cur not in secondaryArgs:
                        throwInvalid(
                            4,
                            f"'{cur}' is not a valid argument for '{argsMap['func']}'",
                        )

                    elif cur in secondaryArgs:
                        argsMap["secondary"] = cur

                else:  # VALID -- 'SEARCH' OR 'LIST' ARGUMENTS
                    if "search" in argsMap.keys():
                        throwInvalid(5, "")

                    elif argsMap["func"] == "list":
                        if cur == "type":
                            argsMap["list"] = "/\\"
                            printBar("listing defined alias types", "")

                        else:
                            printBar(f"attempting to list aliases of type '{cur}'", cur)
                            argsMap["list"] = cur

                    else:
                        printBar(f"searching for '{cur}'", cur)
                        argsMap["search"] = cur

            elif len(argsMap["func"]) < 1:  # no arguments already,
                throwInvalid(1, cur)  # so first arg is unrecognizable

        args.remove(cur)

    return argsMap
