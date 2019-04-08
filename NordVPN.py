import os.path
from shutil import which

import eel

from Connect import Connect
from Functions import Functions
from ConnectButton import ConnectionButton

eel.init('../NordVPNGUI')

NORDVPN = Connect()

# update quickconnect button
UPDATEBUTTON = ConnectionButton(NORDVPN)
UPDATEBUTTON.start()

# update the json file every 30 minutes
UPDATEJSON = Functions()
UPDATEJSON.start()


@eel.expose
def get_connection_status():
    """
    Gets the connection status of the nordVPN client
    :return: boolean
    """
    return NORDVPN.check()


@eel.expose
def get_status():
    """
    Returns the status of the VPN connection
    :return: returns an array with importations         # 0 = connection status
                                                        # 1 = server
                                                        # 2 = country
                                                        # 3 = city
                                                        # 4 = IP
                                                        # 5 = protocol
                                                        # 6 = revived data
                                                        # 7 = send data
                                                        # 8 = duration of the connection
    """
    return NORDVPN.status()


@eel.expose
def quick_connect():
    """
    Calls the quick connect method
    :return: boolean
    """
    if not NORDVPN.disconnecting and not NORDVPN.connecting:
        return NORDVPN.quick_connect()


@eel.expose
def connect_to_location(country, city):
    """
    Calls the connect to location method
    :param country: country you want to connect to
    :param city: city in country you want to connect to
    :return: boolean
    """
    if not NORDVPN.disconnecting and not NORDVPN.connecting:
        return NORDVPN.connect_to_location(country, city)


@eel.expose
def disconnect():
    """
    disconnects from nordVPN
    :return: boolean
    """
    if not NORDVPN.disconnecting and not NORDVPN.connecting:
        return NORDVPN.disconnect()


@eel.expose
def return_countries():
    """
    Get the countries available
    :return: country JSON
    """
    with open("country.json", "r") as country:
        return country.read()


@eel.expose
def return_cities():
    """
    Gets the cities available in the countries
    :return: JSON with countries and cities
    """
    with open("cities.json", "r") as citiy:
        return citiy.read()

@eel.expose
def return_login_status():
    """
    Gets the login status and returns it
    :return: boolean
    """
    return NORDVPN.check_login()


while not os.path.exists("country.json"):
    eel.sleep(1)

while not os.path.exists("cities.json"):
    eel.sleep(1)

if which("chromium"):
    eel.start('server.html', options={'port': 15651})
else:
    eel.start('server.html', options={'mode': 'default', 'host': 'localhost', 'port': 15651,
                                      'chromeFlags': ""})
