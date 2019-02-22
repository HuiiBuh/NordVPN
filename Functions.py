import subprocess
import logging
import json
import threading
import time
from Logger import Logger


# ToDo Die cities in dem cieties dict sortieren


class Functions(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.log = Logger.setup_logger(Logger(), "logger", "Log/log.log", logging.DEBUG, "Log")
        self.error_logger = Logger.setup_logger(Logger(), "Log/error_logger", "error.log", logging.ERROR, "Log")

    def run(self):
        self.execute()

    def execute(self):

        time_st_old = time.time()
        while threading.main_thread().is_alive():
            time.sleep(2)
            if time.time() - time_st_old > 30 * 60:
                temp = self.check_countries()
                self.check_country_city(temp)
                time_st_old = time.time()

    def check_countries(self):
        """Checks the countries that are available in the NordVPV client by reading the shell output"""

        countries = subprocess.check_output(['nordvpn', 'countries']).decode('UTF-8') \
            .replace('\t\t\t', '!').replace('\n', '!').replace('\t\t', '!').replace('\t', '!') \
            .replace('-', '').replace('\r', '').replace('\\', '').replace('|', '') \
            .replace(' ', '').replace('/', '').split('!')

        # removes an empty string
        countries = list(filter(None, countries))

        # sort list
        countries = sorted(countries, key=str.lower)

        with open("country.json", "w") as country:
            country.write(json.dumps(countries))

        return countries

    def check_country_city(self, countries):
        """Takes the countries and checks the available cities in the countries"""

        country_city = {}
        for c in countries:
            country_city[c] = []

        for country in country_city:
            temp_cities = subprocess.check_output(['nordvpn', 'cities', country]).decode('UTF-8') \
                .replace('\t\t', '!').replace('\t', '!').replace('\r', '').replace('|', '') \
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
