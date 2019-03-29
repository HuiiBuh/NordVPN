import eel
import os.path
import time
from shutil import which
from Connect import Connect

from Functions import Functions
from Settings import Settings
from connectButton import ConnectionButton

eel.init('../NordVPNGUI')

nordvpn = Connect()

# update quickconnect button
updateButton = ConnectionButton(nordvpn)
updateButton.start()

# update the json file every 30 minutes
updateJson = Functions()
updateJson.start()


@eel.expose
def get_connection_status():
    return nordvpn.check()


@eel.expose
def get_status():
    return nordvpn.status()


@eel.expose
def quick_connect():
    if not nordvpn.disconnecting and not nordvpn.connecting:
        return nordvpn.quick_connect()


@eel.expose
def connect_to_location(country, city):
    if not nordvpn.disconnecting and not nordvpn.connecting:
        return nordvpn.connect_to_location(country, city)


@eel.expose
def disconnect():
    if not nordvpn.disconnecting and not nordvpn.connecting:
        return nordvpn.disconnect()


@eel.expose
def return_countries():
    with open("country.json", "r") as country:
        return country.read()


@eel.expose
def return_cities():
    with open("cities.json", "r") as citiy:
        return citiy.read()


while not os.path.exists("country.json"):
    eel.sleep(1)

while not os.path.exists("cities.json"):
    eel.sleep(1)

try:
    open("country.json", "r")
except FileNotFoundError:
    pass

try:
    open("cities.json", "r")
except FileNotFoundError:
    pass

if which("chromium"):
    eel.start('server.html', options={'port': 15651})
else:
    eel.start('server.html', options={'mode': 'default', 'host': 'localhost', 'port': 15651, 'chromeFlags': ""})
