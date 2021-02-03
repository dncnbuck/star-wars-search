import sys
import logging
import time
import logging.handlers


def configure_logging(filename=None, debug=False):
    logging.root.handlers = []
    format = "[%(levelname)1.1s %(asctime)s.%(msecs)03dZ] [%(name)s] %(message)s"
    date_format = "%Y-%m-%dT%H:%M:%S"

    level = (logging.DEBUG if debug else logging.INFO)
    formatter = logging.Formatter(fmt=format, datefmt=date_format)

    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(level)
    sh.setFormatter(formatter)

    handlers = [sh]
    if filename:
        fh = logging.FileHandler(filename)
        fh.setLevel(level)
        fh.setFormatter(formatter)
        handlers.append(fh)

    logging.basicConfig(
        level=level,
        format=format,
        handlers=handlers
    )

    logging.Formatter.converter = time.gmtime
