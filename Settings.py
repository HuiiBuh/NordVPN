import subprocess
from Logger import Logger
import logging

# ToDo Implement other settings than the change between UDP and TCP


class Settings:
    def __init__(self):
        self.log = Logger.setup_logger(Logger(), "logger", "Log/log.log", logging.DEBUG, "Log")
        self.error_logger = Logger.setup_logger(Logger(), "Log/error_logger", "error.log", logging.ERROR, "Log")

    def udp_or_tcp(self, protocoltype):
        """Set the Protocol either to UDP or TCP"""
        if protocoltype == "UDP" or protocoltype == "TCP":
            protocol = subprocess.check_output(['nordvpn set protocol', protocoltype])

            if protocoltype in protocol:
                self.log.info("Set the Protocol type to " + protocoltype)
                return True
            else:
                self.log.error("Could not set the Protocol type to " + protocoltype)
                self.error_logger.error("Could not set the Protocol type to " + protocoltype)
                return False
        else:
            self.log.error(protocoltype + "is not a valid option. Only use UDP or TCP")
            self.error_logger.error(protocoltype + "is not a valid option. Only use UDP or TCP")
            return False

    def get(self):
        """Get the current settings of the NordVPN Client"""

        # 0 = Protocol --> UDP == True
        # 1 = Kill Switch
        # 2 = CyberSec --> Can't be enabled if a custom DNS is used
        # 3 = Obfuscate
        # 4 = Auto Connect
        # 5 = DNS

        protocol = subprocess.check_output(['nordvpn', 'settings']).decode('UTF-8').split('\n')

        search = ["TCP", "disabled", "disabled", "disabled", "disabled", "disabled"]
        settings = []

        for i in range(len(search)):
            settings.append(search[i] not in protocol[i])

        return settings
