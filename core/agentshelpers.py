from common import *
from encryption import *

from collections import OrderedDict
from shutil import rmtree
from base64 import b64decode

agents = OrderedDict()

def checkAgentsEmpty(s):
    
    uagents()

    global agents

    if len(agents) == 0:
        
        if s == 1:
            error("There are no active agents.")
            return True
        else:
            return True
    
    else:
        return False

def isValidAgent(name, s):

    uagents()
    vAgents = []
    for agent in agents:
        vAgents.append(agents[agent].name)

    if name in vAgents:
        return True
    else:
        if s == 1:
            error("Invalid agent.")
            return False
        else:
            return False

def viewAgents():

    if checkAgentsEmpty(1) == False:

        success("Active Agents:")
        
        print(YELLOW)
        print(" Name                         Listener                         External IP                         Hostname")
        print("------                       ----------                       -------------                       ----------")
        
        for i in agents:
            print(" {}".format(agents[i].name) + " " * (29 - len(agents[i].name)) + "{}".format(agents[i].listener) + " " * (33 - len(agents[i].listener)) + agents[i].remoteip + " " * (36 - len(agents[i].remoteip)) + agents[i].hostname)
        
        print(cRESET)

def renameAgent(args):

    if len(args) != 2:
        error("Invalid arguments.")
    else:
        
        name    = args[0]
        newname = args[1]

        if isValidAgent(name, 1) == True:
            
            if isValidAgent(newname, 0) == True:
                error("Agent {} already exists.".format(newname))
                return 0
            
            agents[name].rename(newname)
            
            if os.path.exists(agents[name].Path):
                rmtree(agents[name].Path)

            removeFromDatabase(agentsDB, name)
            agents[name].name = newname
            agents[name].update()
            writeToDatabase(agentsDB, agents[name])
            
            uagents()

        else:
            return 0

def removeAgent(args):
    
    if len(args) != 1:
        error("Invalid arguments.")
    else:
        name = args[0]
        if isValidAgent(name, 1):
            taskAgentToQuit(name)
            rmtree(agents[name].Path)
            removeFromDatabase(agentsDB,name)
            uagents()
        else:
            pass

def getAgentsForListener(name):
    
    result = []

    for agent in agents:
        if agents[agent].listener == name:
            result.append(agents[agent].name)

    return result

def interactWithAgent(args):
    
    if len(args) != 1:
        error("Invalid arguments.")
    else:
        name = args[0]
        if isValidAgent(name, 1):
            agents[name].interact()
        else:
            pass

def clearAgentTasks(name):
    if isValidAgent(name, 0):
        agents[name].clearTasks()
    else:
        pass

def displayResults(name, result):

    if isValidAgent(name,0) == True:

        if result == "":
            success("Agent {} completed task.".format(name))
        else:
            
            key = agents[name].key
            
            if agents[name].Type == "p":

                try:
                    plaintext = DECRYPT(result, key)
                except:
                    return 0
            
                if plaintext[:5] == "VALID":
                    success("Agent {} returned results:".format(name))
                    print(plaintext[6:])
                else:
                    return 0
            
            else:
                success("Agent {} returned results:".format(name))
                print(result)
                
def taskAgentToQuit(name):
    agents[name].Quit()

def uagents():
    global agents
    
    try:
        temp = readFromDatabase(agentsDB)
        agents = OrderedDict()
        for agent in temp:
            agents[agent.name] = agent
    except:
        pass
