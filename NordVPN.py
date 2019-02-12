import eel
import time
from ShellConnection import ShellConnections
from ShellFunctions import ShellFunctions
from ShellSettings import ShellSettings

eel.init('../NordVPNGUI')

shellConnect = ShellConnections()


@eel.expose
def get_connection_status():
    return shellConnect.check_connection()

@eel.expose
def get_status():
    return shellConnect.status();

@eel.expose
def quick_connect():
    return shellConnect.quick_connect()


@eel.expose
def disconnect():
    return shellConnect.disconnect();


eel.start('server.html')
