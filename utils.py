
def drawCodes(match: str) -> str:
    tmp = ""
    cases = {
        'tumbo': """    
      /^__^\\
     / .  . \\
    /        \\
   /  \/  \/  \\
   \__________/""",
        'tumboHat': """    
       _____
      |     |
   ___|_____|___
     / .  . \\
    /        \\
   /  \/  \/  \\
   \__________/""",

        'tumboNoArgs': f"""    
     /^__^\     
    / .  . \\
   /        \\\u261E  no args given to Tumbo
  /  \/      \\
  \__________/\n""",
    }
    if match in cases.keys():
        tmp += cases[match]

    return tmp

def drawCodesArg(match: str, arg: str):
    tmp = ""
    cases = {
    'tumboArg': f"""    
     /^__^\     {arg}
    / .  . \\ / 
   /        \\
  /  \/  \/  \\
  \__________/""",
    }
    if match in cases.keys():
        tmp += cases[match]

    return tmp





def throwInvalid(err: int, arg: str):
    errlogs = {
        1: f" {drawCodesArg('tumboArg', arg)}  \n\n error: unrecognized argument\n'{arg}' is not a valid command",
        2: f" {drawCodes('tumbo')} \n\n error: too many function arguments passed",
        3: f" {drawCodes('tumboHat')} \n\n error: 'source' does not take an argument",
        4: f" {drawCodes('tumboHat')} \n\n error: {arg}",
        5: f" {drawCodes('tumboHat')} \n\n error: 'search' does not take multiple arguments",
    }
    print(errlogs[err])
    exit(0)