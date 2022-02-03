import logging
import os
import sys

from main import main

_levels = {
    'info': logging.INFO,
    'debug': logging.DEBUG
}

_level = os.getenv('LOG_LEVEL', 'debug')
_logLevel = _levels[_level]

logger = logging.getLogger()
logger.setLevel(_logLevel)

formatter = logging.Formatter(fmt='%(asctime)s.%(msecs)03d %(levelname)5s %(process)d --- ['
                              '%(threadName)15s] %(name)-40s: %(message)s',
                              datefmt='%Y-%m-%d,%H:%M:%S')
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger.addHandler(handler)

if _level == "debug":
    _output_fn = os.getenv('LOG_FILE', 'generator.log')
    fileHandler = logging.FileHandler(_output_fn)
    fileHandler.setLevel(_logLevel)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)

resources_path = "./resources/"
templates_path = f"{resources_path}templates"
products_path = f"{resources_path}products.txt"
names_path = f"{resources_path}names.csv"
places_path = f"{resources_path}places.csv"
images_path = f"{resources_path}img/"

main(templates_path=templates_path,
     products_path=products_path,
     names_path=names_path,
     places_path=places_path,
     images_path=images_path)
