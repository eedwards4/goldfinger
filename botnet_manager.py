# goldfinger
# created by Ethan Edwards and Collins Senaya

# For bots
from MetaTrader5 import *
import threading


# For UI
# TODO: FIND A PACKAGE FOR GUI (PREFERABLY HTML/JS)

commands = {"help", "new", "list", "start", "kill", "quit"}

class Bot:
    def __init__(self, _name, _dir):
        self.name = _name
        self.fileDir = _dir
        self.status = "Idle"

    def start(self):
        self.status = "Running"
        # Thread setup/start

    def kill(self):
        self.status = "Killed"
        # Proper thread shutdown here

def main():
    b1 = Bot("test", "/home/fake/address")
    bots = [b1]
    # Temp cli interface
    # TODO: REPLACE WITH A GUI
    print("Welcome to the Goldfinger Bot Manager!")
    print("Type 'help' for a list of commands")
    while True:
        command = input("> ")
        if command == "quit":
            print("Shutting down botnet...")
            for bot in bots:
                bot.kill()
            print("All bots exited successfully, exiting")
            exit(0)

        elif command == "help":
            print("Commands:")
            for command in commands:
                print(command)

        elif command == "new":
            print("Please enter a name for the new bot:")
            name = input("> ")
            print("Please enter the bot file location:")
            botDir = input("> ")
            print("Creating {} at {}".format(name, botDir))
            bots.append(Bot(name, botDir))

        elif command == "list":
            for bot in bots:
                print("{} ({})".format(bot.name, bot.status))

        elif command == "kill":
            print("Which bot would you like to kill ?")
            bot_to_kill = input("> ")
            for bot in bots:
                if bot_to_kill == bot.name:
                    bot.kill()
                    print("Bot {} killed".format(bot.name))
                    bots.remove(bot)

        elif command == "start":
            print("Which bot would you like to start ?")
            bot_to_start = input("> ")
            for bot in bots:
                if bot_to_start == bot.name:
                    bot.start()
                    print("Bot {} started".format(bot.name))

        else:
            print("Invalid command")
            print("Type 'help' for a list of commands")


if __name__ == "__main__":
    main()
