import eel
import time
from Connect import Connect
from Functions import Functions
from Settings import Settings

eel.init('../NordVPNGUI')

connection = Connect()


@eel.expose
def get_connection_status():
    return connection.check()


@eel.expose
def get_status():
    return connection.status()


@eel.expose
def quick_connect():
    return connection.quick_connect()


@eel.expose
def connect_to_loaction():
    return connection.connect_to_location()


@eel.expose
def disconnect():
    return connection.disconnect()


eel.start('server.html')
