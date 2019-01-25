import subprocess
import logging
from Logger import Logger


# ToDo Immer wenn man sich verbindet auch noch den Ort an den man sich verbindet hin schrieben
# ToDo Exceptions hinzufügen
# ToDo Geht Zeile 35 auch eleganter

class ShellConnections:

    def __init__(self):

        #self.connection_status = None
        self.log = Logger.setup_logger(Logger(), "logger", "Log/log.log", logging.DEBUG, "Log")
        self.error_logger = Logger.setup_logger(Logger(), "error_logger", "Log/error.log", logging.ERROR, "Log")

    def check_connection(self):
        """Used to check the connection status of the NordVPN client"""

        self.connection_status = subprocess.check_output(['nordvpn', 'status']).decode('UTF-8')
        if "Connected" in self.connection_status:
            return True
        else:
            return False

    def fast_connect(self):
        """Connect to the best location available"""

        if self.check_connection():
            self.disconnect()
#
        if not self.check_connection():
            subprocess.check_output(['nordvpn', 'connect'])
            if self.check_connection():
                self.log.info("You are connected to " + self.status()[2] + "-" + self.status()[3])
                return True
            else:
                self.log.error("Could not fast connect")
                self.error_logger.error("Could not fast connect")
                return False
        else:
            self.log.error("Could not fast connect")
            self.error_logger.error("Could not fast connect")
            return False

    def connect_to_location(self, country, city):
        """Connects to a specific location.
        Assign "" (empty string) to City if you want to connect only to the country"""

        if self.connection_status():
            self.disconnect()

        if not self.connection_status():
            subprocess.check_output(['nordvpn', 'disconnect', country, city])
            if self.connection_status:
                self.log.info("You are connected to " + country + " " + city + " .")
                return True
            else:
                self.log.error("Could not connect to " + country + " " + city + " .")
                self.error_logger.error("Could not connect to " + country + " " + city + " .")
                return False
        else:
            self.log.error("Could not connect to " + country + " " + city + " .")
            self.error_logger.error("Could not connect to " + country + " " + city + " .")
            return False

    def disconnect(self):
        """Disconnects form the NordVPN Client"""

        if self.check_connection():
            subprocess.check_output(['nordvpn', 'disconnect'])
            if not self.check_connection():
                self.log.info("You are disconnected")
                return True
            else:
                self.log.error("You could not disconnect")
                self.error_logger.error("You could not disconnect")
                return False
        else:
            self.log.info("You tried to disconnect even though you are not connected to NordVPN")
            return True

    def status(self):
        status = subprocess.check_output(['nordvpn', 'status']).decode('UTF-8').replace('\r', '').replace('-', '')\
            .replace('  ', '').split('\n')
        status = [x for x in status if x != '']

        return_status = []

        for i in range(len(status)):
            start = status[i].find(':') + 2
            end = len(status[i])
            return_status.append(status[i][start:end])

        # 0 = connection status
        # 1 = server
        # 2 = country
        # 3 = city
        # 4 = IP
        # 5 = protocol
        # 6 = revived data
        # 7 = send data
        # 8 = duration of the connection
        return return_status
