import subprocess
import logging
from Logger import Logger


# ToDo Immer wenn man sich verbindet auch noch den Ort an den man sich verbindet hin schrieben
# ToDo Exceptions hinzufügen

class ShellConnections:

    def __init__(self):
        """Initializes the Loggers of the File"""

        self.connection_status = None
        self.log = Logger.setup_logger(Logger(), "logger", "Log/log.log", logging.DEBUG, "Log")
        self.error_logger = Logger.setup_logger(Logger(), "Log/error_logger", "error.log", logging.ERROR, "Log")

    def check_connection(self):
        """Used to check the connection status of the NordVPN client"""

        self.connection_status = subprocess.check_output(['nordvpn', 'status']).decode("utf-8")
        if "Connected" in self.connection_status:
            return True
        else:
            return False

    def fast_connect(self):
        """Connect to the best location available"""

        if self.connection_status():
            self.disconnect()

        if not self.check_connection():
            subprocess.check_output(['nordvpn', 'connect'])
            if self.check_connection():
                self.log.info("You are connected")
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
            subprocess.check_output(['nordvpn', 'disconnect', str(country), str(city)])
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
