import eel
from shutil import which
from Connect import Connect

import time
from Functions import Functions
from Settings import Settings
from connectButton import ConnectionButton

eel.init('../NordVPNGUI')

# update quickconnect button
updateButton = ConnectionButton()
updateButton.start()

# update the json file every 30 minutes
updateJson = Functions()
updateJson.start()

nordvpn = Connect()


@eel.expose
def get_connection_status():
    return nordvpn.check()


@eel.expose
def get_status():
    return nordvpn.status()


@eel.expose
def quick_connect():
    return nordvpn.quick_connect()


@eel.expose
def connect_to_location(country, city):

    return nordvpn.connect_to_location(country, city)


@eel.expose
def disconnect():
    return nordvpn.disconnect()


@eel.expose
def return_countries():
    with open("country.json", "r") as country:
        return country.read()


@eel.expose
def return_cities():
    with open("cities.json", "r") as citiy:
        return citiy.read()


if which("chromium"):
    eel.start('server.html')
else:
    eel.start('server.html', options={'mode': 'default','host': 'localhost','port': 8000,'chromeFlags': ""})
