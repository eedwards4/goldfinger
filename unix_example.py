# Unix example for goldfinger

from botnet_manager import Manager
import datetime
import sys

def main():
    myBot = Manager()  # Required!

    # User code goes here (Pre-execution)!
    file = open("test_output.txt", "w")
    file.write("Started at: {}".format(datetime.datetime.now()))
    file.write("\n")

    while not myBot.kill_now:  # Required!
        # User code goes here!!
        file.seek(39)
        file.write(" Running")

    # User code goes here (Post-execution)!
    file.write("\nStopped at: {}".format(datetime.datetime.now()))
    file.close()
    exit(0)


if __name__ == '__main__':
    main()
