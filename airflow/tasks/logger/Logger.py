import logging
import json_log_formatter

class Log:
    def __init__(self, name):
        self.current_filename = "logger".rsplit('.', 1)[0]
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        self.formatter = json_log_formatter.JSONFormatter() 

        self.console_handler = logging.StreamHandler()
        self.console_handler.setLevel(logging.DEBUG)
        self.console_handler.setFormatter(self.formatter)

        self.info_file_handler = logging.FileHandler("/opt/airflow/python_log/" + self.current_filename + '_info.log')
        self.info_file_handler.setLevel(logging.INFO)
        self.info_file_handler.setFormatter(self.formatter)

        self.error_file_handler = logging.FileHandler("/opt/airflow/python_log/" + self.current_filename + '_error.log')
        self.error_file_handler.setLevel(logging.ERROR)
        self.error_file_handler.setFormatter(self.formatter)

        self.critical_file_handler = logging.FileHandler("/opt/airflow/python_log/" + self.current_filename + '_critical.log')
        self.critical_file_handler.setLevel(logging.CRITICAL)
        self.critical_file_handler.setFormatter(self.formatter)

        self.logger.addHandler(self.console_handler)
        self.logger.addHandler(self.info_file_handler)
        self.logger.addHandler(self.error_file_handler)
        self.logger.addHandler(self.critical_file_handler)