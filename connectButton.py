import eel
import threading
import time
from Connect import Connect

# ToDo schön das Programm beenden


class ConnectionButton (threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.interrupt = False
        self.connect = Connect()

    def run(self):
        self.get_statue_of_connection()

    def get_statue_of_connection(self):
        while threading.main_thread().is_alive():
            if not self.interrupt:
                detailed_state = self.connect.status()
                state = self.connect.check()
                eel.updateStatus(detailed_state, state)
                time.sleep(1)
            else:
                pass
