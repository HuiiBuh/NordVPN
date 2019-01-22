import logging
import os


class Logger:
    """Creates an Object Logger. There are two loggers to be instanced. The error log for all error messages and the
    information log in which all user interactions and errors are logged"""

    def __init__(self):
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', "%Y-%m-%d %H:%M:%S")

    def setup_logger(self, name, log_file, level, directory):
        """Creates and returns a logger"""

        if not os.path.exists(directory):
            os.makedirs(directory)


        handler = logging.FileHandler(log_file)
        handler.setFormatter(self.formatter)

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        return logger
