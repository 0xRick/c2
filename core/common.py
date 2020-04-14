import pickle
import os
from collections import OrderedDict

RED     = "\u001b[31m"
GREEN   = "\u001b[32m"
YELLOW  = "\u001b[33m"
cRESET  = "\u001b[0m"

listenersDB = "data/databases/listeners.db"
agentsDB    = "data/databases/agents.db"

def prompt(name):
    
    prompt = "\n" + GREEN + "(" + name + ")" + RED + "::> " + cRESET
    return prompt

def error(message):
    
    print("\n" + RED + "[!] " + message + cRESET)

def success(message):
    
    print("\n" + GREEN + "[*] " + message + "\n" + cRESET)

def progress(message):
    
    print("\n" + YELLOW + "[*] " + message + "\n" + cRESET)

def readFromDatabase(database):
    
    data = []

    with open(database, 'rb') as d:
        
        while True:
            try:
                data.append(pickle.load(d))
            except EOFError:
                break
    
    return data

def writeToDatabase(database,newData):
    
    with open(database, "ab") as d:
        pickle.dump(newData, d, pickle.HIGHEST_PROTOCOL)

def removeFromDatabase(database,name):
    
    data = readFromDatabase(database)
    final = OrderedDict()

    for i in data:
        final[i.name] = i
    
    del final[name]
    
    with open(database, "wb") as d:
        for i in final:
            pickle.dump(final[i], d , pickle.HIGHEST_PROTOCOL)

def clearDatabase(database):

    if os.path.exists(database):
        os.remove(database)
    else:
        pass
