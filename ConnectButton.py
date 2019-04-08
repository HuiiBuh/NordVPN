import threading
import time

import eel

from Connect import Connect


class ConnectionButton(threading.Thread):
    """
    Calls the connectButton of the GUI every second to update the message
    """
    def __init__(self, nordvpn):
        threading.Thread.__init__(self)
        self.nordvpn = nordvpn

        self.connect = Connect()

    def run(self):
        self.set_statue_of_connection_gui()

    def set_statue_of_connection_gui(self):
        """
        Call method of the connectbutton in js to update the connectbutton
        :return: None
        """
        while threading.main_thread().is_alive():

            if not self.nordvpn.connecting and not self.nordvpn.disconnecting:
                detailed_state = self.connect.status()
                state = self.connect.check()
                eel.updateStatus(detailed_state, state)
            elif self.nordvpn.connecting:
                eel.updateStatus("Connecting", "Connecting")
            elif self.nordvpn.disconnecting:
                eel.updateStatus("Disconnecting", "Disconnecting")
            time.sleep(1)
