from configparser import ConfigParser
from urllib.parse import quote
from os import path, getenv

import logging
from pythonjsonlogger import jsonlogger


def get_logger():
    logger = logging.getLogger()
    configurations = get_configurations()

    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter()
    logHandler.setFormatter(formatter)
    if (logger.hasHandlers()):
        logger.handlers.clear()

    logger.addHandler(logHandler)
    logger.setLevel(getattr(logging,
                            configurations.get("logging", "level")))
    return logger


def get_configurations():
    configuration = ConfigParser()
    APPLICATION_ROOT_PATH = path.abspath(
        path.join(path.dirname(__file__), ".."))

    configuration.read(
        path.join(APPLICATION_ROOT_PATH,
                  "config",
                  "default.toml"))
    return configuration


def get_database_connection():
    CONFIGURATIONS = get_configurations()
    CONFIGURATIONS.set("database",
                       "username",
                       getenv("POSTGRES_USER",
                              CONFIGURATIONS.get("database", "username")))
    CONFIGURATIONS.set("database",
                       "password",
                       quote(getenv("POSTGRES_PASSWORD",
                                    CONFIGURATIONS.get("database",
                                                       "password")))
                       .replace("%", "%%"))
    return CONFIGURATIONS.get("database", "connection_string")
