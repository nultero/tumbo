
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
        print('newp')

    def Ls(self):
        print('lsp')

    def Search(self):
        print('searches')

    def All(self):

        # proviso

        self.New()
        self.Ls()
        self.Search()