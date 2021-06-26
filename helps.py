class Helper:
    def __init__(self, rg: str, args: dict):
        self.args = args
        helpSet = {
            "new": self.New,
            "list": self.Ls,
            "search": self.Search,
            "source": self.Source,
            "remove": self.Remove,
            "update": self.Update,
            "*": self.All,
        }
        helpSet[rg]()

    def New(self):
        print("\n*  tumbo NEW [ alias, type, none ]")
        print("\t'alias' : writes alias to a type, after prompting for type")
        print("\t'type'  : defines new file for kind of alias to track")
        print("\t none   : checks and asks for type, writes alias to type")

    def Ls(self):
        print("\n*  tumbo LIST [ type, {string}, none ]")
        print("\t none     : tries to list ALL aliases")
        print("\t'type'    : lists defined alias types in CONFIG dir")
        print("\t{string}  : tries to validate string as type in CONFIG dir,")
        print("\t            and if so, will list aliases under this type")
        print(f"\t>>> CONFIG_PATH : {self.args['conf']}")

    def Search(self):
        print("\n*  tumbo SEARCH [ {string} ]")
        print("\t{string}  : searches for {string} in order:")
        print("\t            type, alias, content")

    def Source(self):
        print("\n*  tumbo SOURCE")
        print("\t(no args) : unpacks all aliases to DEFAULT_SHELL_SOURCE_PATH")
        print(f"\t>>> SOURCE_PATH : {self.args['source']}")

    def Remove(self):
        print("\n*  tumbo REMOVE [ alias, type ]")
        print("\t'alias' : prompts for & deletes line for given alias")
        print("\t'type'  : prompts for & deletes entire alias type, after confirmation")

    def Update(self):
        print("\n*  tumbo UPDATE [ alias, type ]")
        print("\t'alias' : prompts for & edits alias content")
        print("\t'type'  : prompts for & alters type name in DEFAULT_CONFIG_DIR_PATH")

    def All(self):
        self.New()
        self.Ls()
        self.Search()
        self.Source()
        self.Remove()
        self.Update()
