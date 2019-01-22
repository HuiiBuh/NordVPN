from ShellConnection import ShellConnections
from ShellFunctions import ShellFunctions


def on_connection(connection_status):
    print(connection_status)


def on_login(login_status):
    print(login_status)


if __name__ == "__main__":

    """ 
    shell = ShellConnections()
    shell.fast_connect()
    shell.check_connection()
    shell.disconnect()"""

    shell_functions = ShellFunctions(None)
    countries = shell_functions.check_countries()
    shell_functions.check_country_city(countries)

