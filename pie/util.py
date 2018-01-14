import json
import logging
import os
import sys

RESOURCE_FILE = os.getenv('PIE_RESOURCE_CONFIG', "pie_resources.json")
JSON_CONFIG = json.load(open(RESOURCE_FILE))
#programs = json_config['programs']
#genomes = json_config['genomes']
#keys = json_config['keys']
#targets = json_config['targets']
#config = json_config['config']
FORMAT = '%(asctime)-15s %(funcName)-8s %(levelname)s %(message)s'
OUT_HANDLAR = logging.StreamHandler(sys.stdout)
OUT_HANDLAR.setFormatter(logging.Formatter(FORMAT))
OUT_HANDLAR.setLevel(logging.INFO)
LOGGER = logging.getLogger('pie')
LOGGER.addHandler(OUT_HANDLAR)
LOGGER.setLevel(logging.INFO)
