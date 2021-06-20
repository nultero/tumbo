
class Helper:

    def __init__(self, rg: str):

        helpSet = {
            'new': self.New,
            'list': self.Ls,
            'search': self.Search,
            '*': self.All,
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

    def Search(self):
        print('searches')

    def All(self):

        # proviso

        self.New()
        self.Ls()
        self.Search()