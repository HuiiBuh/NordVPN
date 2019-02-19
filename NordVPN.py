#ToDo Auch die Länder müssen in einer JSON Datei gespeichert werden

import eel
from Connect import Connect

import time
from Functions import Functions
from Settings import Settings
from connectButton import ConnectionButton

eel.init('../NordVPNGUI')


thead = ConnectionButton()
thead.start()

temp = Functions()
a = temp.check_countries()

temp.check_country_city(a)


with open("cities.json", "r") as f:
    print(f.read())


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

eel.start('server.html')
