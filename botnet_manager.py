# goldfinger
# created by Ethan Edwards and Collins Senaya

# For bots
import subprocess as sp
import signal
import sys

# For UI
# TODO: FIND A PACKAGE FOR GUI (PREFERABLY HTML/JS)

# IMPORT MODULES. EVERYTHING BETWEEN THIS AND THE BOTTOM COMMENT IS USER-ACCESSIBLE
class Manager:  # TODO: MOVE MORE OF THE MODULE HERE SO LESS USER REQS
    kill_now = False

    def __init__(self):
        if sys.platform == 'darwin' or sys.platform == 'linux':
            signal.signal(signal.SIGINT, self.exit)
            signal.signal(signal.SIGTERM, self.exit)

    def exit(self, signum, frame):
        self.kill_now = True
# IMPORT MODULES. EVERYTHING ABOVE THIS IS USER-ACCESSIBLE

# Internal
commands = {"help", "new", "list", "start", "kill", "quit"}

class Bot:
    def __init__(self, _name, _dir):
        self.process = None
        self.name = _name
        self.fileDir = _dir
        self.status = "Idle"

    def start(self):
        self.status = "Running"
        # Thread setup/start
        self.process = sp.Popen([sys.executable, self.fileDir], stdin=sp.PIPE)

    def kill(self):
        # Proper thread shutdown here
        if self.status == "Running":
            self.status = "Killed"
            if sys.platform == "win32":
                self.process.stdin.write(b'kill\n')  # Windows
                self.process.stdin.flush()
            elif sys.platform == "darwin":
                self.process.send_signal(signal.SIGTERM)  # Macos
            else:
                self.process.send_signal(signal.SIGTERM)  # Linux
            try:
                self.process.wait(10)
            except sp.TimeoutExpired:
                print("Unable to gracefully shut down {}, force killing...".format(self.name))
                self.process.kill()  # Kill process if we can't shut down gracefully

def main():
    ADDEXAMPLES = True
    if ADDEXAMPLES:
        if sys.platform == "win32":
            b1 = Bot("Example", "./Examples/win32_example.py")
        else:
            b1 = Bot("Example", "./Examples/unix_example.py")
        bots = [b1]
    # Temp cli interface
    # TODO: REPLACE WITH A GUI
    print("Welcome to the Goldfinger Bot Manager!")
    print("Type 'help' for a list of commands")
    while True:
        command = input("> ")
        if command in commands:
            if command == "help":
                print("Available commands:")
                for command in commands:
                    print("\t", command)

            elif command == "quit":
                print("Quitting!")
                print("Attempting botnet shutdown...")
                for bot in bots:
                    if bot.status != "Killed":
                        print("Attempting to kill {}".format(bot.name))
                        bot.kill()
                print("Bot shutdown successful. Terminating manager.")
                exit(0)

            elif command == "list":
                for bot in bots:
                    print("{} ({})".format(bot.name, bot.status))

            elif command == "new":
                name = input("Name: ")
                dirname = input("Directory: ")
                bot = Bot(name, dirname)
                bots.append(bot)
                print("Created {} at {}".format(bot.name, bot.fileDir))

            elif command == "start":
                name = input("Name: ")
                for bot in bots:
                    if bot.name == name:
                        bot.start()
                        print("Started {} at {}".format(bot.name, bot.fileDir))

            elif command == "kill":
                target = input("Target: ")
                for bot in bots:
                    if bot.name == target:
                        print("Attempting to kill {}".format(bot.name))
                        bot.kill()
                        print("{} killed successfully.".format(target))

        else:
            print("Invalid command!")


if __name__ == "__main__":
    main()
