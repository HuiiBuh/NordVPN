import eel
import threading
import time
from Connect import Connect


class ConnectionButton(threading.Thread):

    def __init__(self, nordvpn):
        threading.Thread.__init__(self)
        self.nordvpn = nordvpn

        self.connect = Connect()

    def run(self):
        self.get_statue_of_connection()

    def get_statue_of_connection(self):
        while threading.main_thread().is_alive():

            if not self.nordvpn.connecting:
                detailed_state = self.connect.status()
                state = self.connect.check()
                eel.updateStatus(detailed_state, state)
            else:
                eel.updateStatus("Connecting", "Connecting")
            time.sleep(0.1)
