import os
import logging
from configparser import ConfigParser

logger = logging.getLogger(__name__)


def load_config(config_path=None):
    config = Config
    if config_path:
        logger.info("Adding config location: {}".format(config_path))
        config.locations.insert(0, config_path)
    return config.load_config()


class Config:

    locations = [
        "../config/swsearch.cfg",
        "./config/swsearch.cfg",
    ]

    __config__ = None

    def __init__(self):
        pass

    @classmethod
    def load_config(cls) -> 'ConfigParser':
        if cls.__config__ is None:
            for location in cls.locations:
                abs_location = os.path.abspath(location)
                if not os.path.exists(abs_location):
                    continue
                with open(abs_location, 'r') as fd:
                    parser = ConfigParser()
                    parser.read_file(fd)
                    cls.__config__ = parser
                    logger.info("Loaded config Location: {}".format(abs_location))

            if cls.__config__ is None:
                raise OSError("Can't find config in following locations: {}".format(
                    " ".join([os.path.abspath(p) for p in cls.locations]))
                )
        return cls.__config__
