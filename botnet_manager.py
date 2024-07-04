# goldfinger
# created by Ethan Edwards and Collins Senaya

# For bots
import subprocess as sp
import signal
import sys

# For UI
# TODO: FIND A PACKAGE FOR GUI (PREFERABLY HTML/JS)

# Globals
HEADLESS = False
bots = []

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
COMMANDS = {"help", "new", "list", "start", "kill", "quit"}

class Bot:
    def __init__(self, _name, _dir):
        self.process = None
        self.name = _name
        self.fileDir = _dir
        self.status = "Idle"

    def start(self):
        self.status = "Running"
        # Thread setup/start
        try:
            self.process = sp.Popen([sys.executable, self.fileDir], stdin=sp.PIPE)
        except exception as e:
            if HEADLESS:
                print("Error starting bot: {}".format(e))
            self.status = "Error"
            return


    def kill(self):
        # Proper thread shutdown here
        if self.status == "Running":
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
                if HEADLESS:
                    print("Unable to gracefully shut down {}, force killing...".format(self.name))
                self.process.kill()  # Kill process if we can't shut down gracefully
            self.status = "Killed"

class commands:
    def help(self):
        if HEADLESS:
            print("Available commands:")
            for command in COMMANDS:
                print("\t", command)
        else:
            pass

    def quit(self):
        if HEADLESS:
            print("Quitting!")
            print("Attempting botnet shutdown...")

        for bot in bots:
            if bot.status != "Killed":
                bot.kill()

        if HEADLESS:
            print("Bot shutdown successful. Terminating manager.")

        exit(0)

    def list(self):
        if HEADLESS:
            for bot in bots:
                print("{} ({})".format(bot.name, bot.status))
        else:
            pass

    def new(self):
        if HEADLESS:
            name = input("Name: ")
            dirname = input("Directory: ")
            bot = Bot(name, dirname)
            global bots
            bots.append(bot)
            print("Created {} at {}".format(bot.name, bot.fileDir))
        else:
            pass

    def start(self):
        if HEADLESS:
            name = input("Name: ")
            for bot in bots:
                if bot.name == name:
                    bot.start()
                    print("Started {} at {}".format(bot.name, bot.fileDir))

    def kill(self):
        if HEADLESS:
            target = input("Target: ")
            for bot in bots:
                if bot.name == target:
                    print("Attempting to kill {}".format(bot.name))
                    bot.kill()
                    print("{} killed successfully.".format(target))
        else:
            pass


def headless(bots, c):
    print("Welcome to the Goldfinger Bot Manager!")
    print("Type 'help' for a list of commands")
    while True:
        command = input("> ")
        if command in COMMANDS:
            if command == "help":
                c.help()

            elif command == "quit":
                c.quit()

            elif command == "list":
                c.list()

            elif command == "new":
                c.new()

            elif command == "start":
                c.start()

            elif command == "kill":
                c.kill()

        else:
            print("Invalid command!")

def main():
    ADDEXAMPLES = False
    # Create a commands instance
    c = commands()
    # Parse arguments
    if len(sys.argv) > 1:
        for arg in sys.argv:
            if arg == "--examples" or arg == "-e":
                ADDEXAMPLES = True
            if arg == "--headless" or arg == "-h":
                global HEADLESS
                HEADLESS = True
    if ADDEXAMPLES:
        if sys.platform == "win32":
            b1 = Bot("Example", "./Examples/win32_example.py")
        else:
            b1 = Bot("Example", "./Examples/unix_example.py")
        global bots
        bots = [b1]
    # CLI interface
    if HEADLESS:
        headless(bots, c)
    # GUI interface
    else:
        pass  # TODO: GUI INTERFACE


if __name__ == "__main__":
    main()
