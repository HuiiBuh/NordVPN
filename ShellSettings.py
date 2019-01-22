import subprocess

# ToDo Log

class ShellSettings:
    def __init__(self):
        pass


    def UTF_or_TCP(self, protocoltype):
        """Set the Protocol either to UDP or TCP"""
        if protocoltype == "UDP" or protocoltype == "TCP":
            protocol = subprocess.check_output(['nordvpn set protocol', protocoltype])

            if protocol == protocoltype:
                return True
            else:
                return False
        else:
            #error log
            pass

    def get_settings(self):
        """Get the current settings of the NordVPN Client"""

        # 0 = Protocol --> UDP == True
        # 1 = Kill Switch
        # 2 = CyberSec
        # 3 = Obfuscate
        # 4 = Auto Connect
        # 5 = DNS

        protocol = subprocess.check_output(['nordvpn', 'settings']).decode("UTF-8").split('\n')

        search = ["UDP", "disabled", "disabled", "disabled", "disabled", "disabled"]
        settings = []


        for i in range(len(settings)):
            settings.append(search[i] in protocol[i])

        return settings
