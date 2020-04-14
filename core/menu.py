import readline
from collections import OrderedDict
from os import system

from common import *

from listenershelpers import *
from agentshelpers import *
from payloadshelpers import *

class AutoComplete(object):
    
    def __init__(self, options):
        self.options = sorted(options)
        return

    def complete(self, text, state):
        response = None
        if state == 0:

            if text:
                self.matches = [s 
                                for s in self.options
                                if s and s.startswith(text)]
            else:
                self.matches = self.options[:]
        
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response

class Menu:

    def __init__(self, name):

        self.name = name
        
        self.commands = OrderedDict()
        self.Commands = []

        self.commands["help"] = ["Show help.", ""]
        self.commands["home"] = ["Return home.", ""]
        self.commands["exit"] = ["Exit.", ""]

    def registerCommand(self, command, description, args):

        self.commands[command] = [description, args]

    def showHelp(self):

        success("Avaliable commands: ")
        
        print(YELLOW)
        print(" Command                         Description                         Arguments")
        print("---------                       -------------                       -----------")

        for i in self.commands:
            print(" {}".format(i) + " " * (32 - len(i)) + "{}".format(self.commands[i][0]) + " " * (36 - len(self.commands[i][0])) + "{}".format(self.commands[i][1]))
        
        print(cRESET)
    
    def clearScreen(self):
        system("clear")

    def uCommands(self):
        for i in self.commands:
            self.Commands.append(i)

    def parse(self):
        
        readline.set_completer(AutoComplete(self.Commands).complete)
        readline.parse_and_bind('tab: complete')

        cmd = input(prompt(self.name))

        cmd = cmd.split()
        
        command = cmd[0]
        args = []

        for i in range(1,len(cmd)):
            args.append(cmd[i])
        
        return command, args




def evListeners(command, args):

    if command == "list":
        viewListeners()
    
    elif command == "start":
        startListener(args)

    elif command == "stop":
        stopListener(args)
    
    elif command == "remove":
        removeListener(args)

def evAgents(command, args):

    if command == "list":
        viewAgents()
    elif command == "remove":
        removeAgent(args)
    elif command == "rename":
        renameAgent(args)
    elif command == "interact":
        interactWithAgent(args)

def evPayloads(command, args):

    if command == "help":
        Pmenu.showHelp()
    elif command == "home":
        home()
    elif command == "exit":
        Exit()
    elif command == "list":
        viewPayloads()
    elif command == "generate":
        generatePayload(args)

def evHome(command, args):

    if command == "help":
        Hmenu.showHelp()
    elif command == "home":
        home()
    elif command == "listeners":
        listenersHelper()
    elif command == "agents":
        agentsHelper()
    elif command == "payloads":
        payloadsHelper()
    elif command == "exit":
        Exit()


def listenersHelper():
    
    Lmenu.clearScreen()
    
    while True:
        
        try:
            command, args = Lmenu.parse()
        except:
            continue

        if command not in ListenersCommands:
            error("Invalid command.")
        elif command == "home":
            home()
        elif command == "help":
            Lmenu.showHelp()
        elif command == "exit":
            Exit()
        else:
            evListeners(command, args)

def agentsHelper():
    
    Amenu.clearScreen()

    while True:
        
        try:
            command, args = Amenu.parse()
        except:
            continue
            
        if command not in AgentsCommands:
            error("Invalid command.")
        elif command == "home":
            home()
        elif command == "help":
            Amenu.showHelp()
        elif command == "exit":
            Exit()
        else:
            evAgents(command, args)

def payloadsHelper():

    Pmenu.clearScreen()

    while True:
        
        try:
            command, args = Pmenu.parse()
        except:
            continue
            
        if command not in PayloadsCommands:
            error("Invalid command.")
        else:
            evPayloads(command, args)

def home():

    Hmenu.clearScreen()

    while True:
        
        try:
            command, args = Hmenu.parse()
        except:
            continue

        if command not in homeCommands:
            error("Invalid command.")
        else:
            evHome(command, args)

def Exit():
    saveListeners()
    exit()

Amenu = Menu("agents")
Lmenu = Menu("listeners")
Pmenu = Menu("payloads")
Hmenu = Menu("c2")

Amenu.registerCommand("list", "List active agents.", "")
Amenu.registerCommand("interact", "Interact with an agent.", "<name>")
Amenu.registerCommand("rename", "Rename agent.", "<agent> <new name>")
Amenu.registerCommand("remove", "Remove an agent.", "<name>")

Lmenu.registerCommand("list", "List active listeners.", "")
Lmenu.registerCommand("start", "Start a listener.", "<name> <port> <interface> | <name>")
Lmenu.registerCommand("stop", "Stop an active listener.","<name>")
Lmenu.registerCommand("remove", "Remove a listener.", "<name>")

Pmenu.registerCommand("list", "List available payload types.", "")
Pmenu.registerCommand("generate", "Generate a payload", "<type> <arch> <listener> <output name>")

Hmenu.registerCommand("listeners", "Manage listeners.", "")
Hmenu.registerCommand("agents", "Manage active agents.", "")
Hmenu.registerCommand("payloads", "Generate payloads.", "")

Amenu.uCommands()
Lmenu.uCommands()
Pmenu.uCommands()
Hmenu.uCommands()

AgentsCommands    = Amenu.Commands
ListenersCommands = Lmenu.Commands
PayloadsCommands  = Pmenu.Commands
homeCommands      = Hmenu.Commands