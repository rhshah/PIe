#!/usr/bin/env python
# encoding: utf-8
"""
util.py

Created by Ronak Shah on April 12, 2018.
Copyright (c) 2018 Northwell Health. All rights reserved.
"""
import json
import logging
import os
import sys

RESOURCE_FILE = os.getenv('PIE_RESOURCE_CONFIG', "pie_resources.json")
JSON_CONFIG = json.load(open(RESOURCE_FILE))
programs = JSON_CONFIG['programs']
genomes = JSON_CONFIG['genomes']
chr1_fingerprints = JSON_CONFIG['chr1_fingerprints']
keys = JSON_CONFIG['keys']
targets = JSON_CONFIG['targets']
config = JSON_CONFIG['config']
FORMAT = '%(asctime)-15s %(funcName)-8s %(levelname)s %(message)s'
OUT_HANDLAR = logging.StreamHandler(sys.stdout)
OUT_HANDLAR.setFormatter(logging.Formatter(FORMAT))
OUT_HANDLAR.setLevel(logging.INFO)
LOGGER = logging.getLogger('pie')
LOGGER.addHandler(OUT_HANDLAR)
LOGGER.setLevel(logging.INFO)


