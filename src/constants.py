"""
Fully-qualified paths, parsed configurations
and other global variables.
"""

import os
import yaml
import json
import logging

##################################################
# paths
##################################################

CONSTANTS_FILE = os.path.abspath(__file__)
SRC_DIR        = os.path.dirname(CONSTANTS_FILE)
PROJECT_DIR    = os.path.dirname(SRC_DIR)

CONF_DIR         = os.path.join(PROJECT_DIR, "conf")
CONF_TEMPER_FILE = os.path.join(CONF_DIR, "temper.yml")

ELASTIC_DIR           = os.path.join(PROJECT_DIR, "elastic")
ELASTIC_POLICY_FILE   = os.path.join(ELASTIC_DIR, "lifecycle_policy.json")
ELASTIC_TEMPLATE_FILE = os.path.join(ELASTIC_DIR, "index_template.json")

##################################################
# read configurations
##################################################

with open(CONF_TEMPER_FILE, "r", encoding="utf-8") as conf_temper_opened:
    CONF_TEMPER_YAML = yaml.safe_load(conf_temper_opened)["temper"]

with open(ELASTIC_POLICY_FILE, "r", encoding="utf-8") as elastic_policy_opened:
    ELASTIC_POLICY_JSON = json.loads(elastic_policy_opened)

with open(ELASTIC_TEMPLATE_FILE, "r", encoding="utf-8") as elastic_template_opened:
    ELASTIC_TEMPLATE_JSON = json.loads(elastic_template_opened)

##################################################
# logging
##################################################

LOGGING_FORMAT_BANNER = CONF_TEMPER_YAML["logging"]["format"]["banner"]
LOGGING_FORMAT_DATE   = CONF_TEMPER_YAML["logging"]["format"]["date"]
LOGGING_FORMAT_TIME   = CONF_TEMPER_YAML["logging"]["format"]["time"]

logging.basicConfig(
    format=LOGGING_FORMAT_BANNER,
    datefmt=LOGGING_FORMAT_DATE + " " + LOGGING_FORMAT_TIME + " Z",
    level=logging.INFO
)

ELASTIC_LOG = logging.getLogger("elastic_transport")
ELASTIC_LOG.setLevel(logging.CRITICAL)

##################################################
# general
##################################################

LOOP_INTERVAL       = CONF_TEMPER_YAML["loop_interval"]
DOC_FORMAT_TIMEDATE = LOGGING_FORMAT_DATE + "T" + LOGGING_FORMAT_TIME + "Z"
UNIT                = CONF_TEMPER_YAML["unit"]
