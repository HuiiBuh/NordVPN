import subprocess
from threading import Thread
import logging
import json
from Logger import Logger

# ToDo Soll jede Funktion prüfen, ob sie auch ausgeführt werden darf?

class ShellFunctions(Thread):

    def __init__(self, on_login):
        Thread.__init__(self)
        self.on_login = on_login
        self.login_status = None

        self.connection_status = None
        self.log = Logger.setup_logger(Logger(), "logger", "Log/log.log", logging.DEBUG, "Log")
        self.error_logger = Logger.setup_logger(Logger(), "Log/error_logger", "error.log", logging.ERROR, "Log")

    def run(self):
        self.check_login()

    def check_login(self):
        """Checks if you are connected to the NordVPN client"""

        self.login_status = subprocess.check_output(['nordvpn', 'login']).decode('UTF-8')
        if "logged in" in self.login_status:
            self.log.info("You are logged in.")
            self.on_login(True)
        else:
            self.log.info("You are not logged in.")
            self.on_login(False)

    def check_countries(self):
        """Checks the countries that are available in the NordVPV client by reading the shell output"""

        countries = subprocess.check_output(['nordvpn', 'countries']).decode('UTF-8') \
            .replace('\t\t\t', '!').replace('\n', '!').replace('\t\t', '!').replace('\t', '!') \
            .replace('-', '').replace('\r', '').replace('\\', '').replace('|', '') \
            .replace(' ', '').replace('/', '').split('!')

        # removes an empty string at the end of the list
        del countries[len(countries) - 1]
        return countries

    def check_country_city(self, countries):
        """Takes the countries and checks the available cities in the countries"""

        country_city = {}
        for c in countries:
            country_city[c] = []

        for country in country_city:
            temp_cities = subprocess.check_output(['nordvpn', 'cities', country]).decode('UTF-8') \
                .replace('\t\t', '!').replace('\t', '!').replace('\r', '').replace('|', '')\
                .replace('-', '').replace(',', '').replace('\n', '').replace(' ', '') \
                .replace('\\', '').replace('/', '').split('!')
            cities = []
            if "error" not in temp_cities:
                for city in temp_cities:
                    if city != "":
                        cities.append(city)
            else:
                self.log.error("There was an error in the city list.")
                self.error_logger.error("There was an error in the city list")

            country_city[country] = cities
        with open("cities.json", "w") as cities:
            cities.write(json.dumps(country_city))




        self.log.info("Working")
        return country_city


