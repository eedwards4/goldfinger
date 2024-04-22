# Win32 Example bot for goldfinger
from botnet_manager import Manager
import threading
import datetime
import sys

class MyBot(Manager):
    def __init__(self):  # Required!
        super().__init__()
        self.sigExit = threading.Lock()
        self.sigExit.acquire()
        work_thread = threading.Thread(target=self.work_loop)
        work_thread.start()
        while True:
            try:
                line = sys.stdin.readline().strip()
                if line == "kill":
                    self.sigExit.release()
                    work_thread.join()
                    break
            except EOFError:
                pass
            except KeyboardInterrupt:
                self.sigExit.release()
                work_thread.join()
                break

    def idle_work(self):
        self.file.seek(39)
        self.file.write(" Running")

    def work_loop(self):
        # User code goes here (Pre-execution)!
        self.file = open("test_output.txt", "w")
        self.file.write("Started at: {}".format(datetime.datetime.now()))
        self.file.write("\n")
        while not self.sigExit.acquire(blocking=False):  # Required!
            # User code goes here!!
            self.idle_work()

        # User code goes here (Post-execution)!
        self.file.write("\nStopped at: {}".format(datetime.datetime.now()))
        self.file.close()
        exit(0)

if __name__ == '__main__':
    bot = MyBot()
