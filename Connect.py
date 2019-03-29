import subprocess
import logging
from Logger import Logger


# ToDo Exceptions hinzufügen

class Connect:

    def __init__(self):

        self.log = Logger.setup_logger(Logger(), "logger", "Log/log.log", logging.DEBUG, "Log")
        self.error_logger = Logger.setup_logger(Logger(), "Log/error_logger", "Log/error.log", logging.ERROR, "Log")
        self.connecting = False
        self.disconnecting = False

    def check_login(self):
        """Checks if you are connected to the NordVPN client"""

        login_status = subprocess.check_output(['nordvpn', 'login']).decode('UTF-8')
        if "logged in" in self.login_status:
            self.log.info("You are logged in.")
            self.on_login(True)
        else:
            self.log.info("You are not logged in.")
            self.on_login(False)

    def check(self):
        """Used to check the connection status of the NordVPN client"""

        connection_status = subprocess.check_output(['nordvpn', 'status']).decode('UTF-8')
        if "Connected" in connection_status:
            return True
        else:
            return False

    def quick_connect(self):
        """Connect to the best location available"""

        self.connecting = True;
        if self.check():
            self.disconnect()

        if not self.check():
            subprocess.check_output(['nordvpn', 'connect'])
            if self.check():
                nordvpn_status = self.status()
                self.log.info("You are connected to " + nordvpn_status[2] + "-" + nordvpn_status[3])
                self.connecting = False
                return True
            else:
                self.log.error("Could not fast connect")
                self.error_logger.error("Could not fast connect")
                self.connecting = False
                return False
        else:
            self.log.error("Could not fast connect")
            self.error_logger.error("Could not fast connect")
            self.connecting = False
            return False


    def connect_to_location(self, country, city):
        """Connects to a specific location.
        Assign "" (empty string) to City if you want to connect only to the country"""

        self.connecting = True
        if self.check():
            self.disconnect()

        if not self.check():
            subprocess.check_output(['nordvpn', 'connect', country, city])
            if self.check():
                self.log.info("You are connected to " + country + " " + city + " .")
                self.connecting = False
                return True
            else:
                self.log.error("Could not connect to " + country + " " + city + " .")
                self.error_logger.error("Could not connect to " + country + " " + city + " .")
                self.connecting = False
                return False
        else:
            self.log.error("Could not connect to " + country + " " + city + " , because you were not disconnected.")
            self.error_logger.error("Could not connect to " + country + " " + city + " ,because you were not "
                                                                                   "disconnected.")
            self.connecting = False
            return False

    def disconnect(self):
        """Disconnects form the NordVPN Client"""

        self.disconnecting = True
        if self.check():
            subprocess.check_output(['nordvpn', 'disconnect'])
            if not self.check():
                self.log.info("You are disconnected")
                self.disconnecting = False
                return True
            else:
                self.log.error("You could not disconnect")
                self.error_logger.error("You could not disconnect")
                self.disconnecting = False
                return False
        else:
            self.log.info("You tried to disconnect even though you are not connected to NordVPN")
            self.disconnecting = False
            return True

    def status(self):
        status = subprocess.check_output(['nordvpn', 'status']).decode('UTF-8').replace('\r', '').replace('-', '') \
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
