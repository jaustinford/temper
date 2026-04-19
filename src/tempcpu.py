"""
Find the hottest CPU temperature and
send to Elasticsearch index.
"""

import os
import platform
from datetime import datetime, timezone
import psutil

import constants
import elastic

def grab_hottest_core():
    """
    Return the temperature in Celsius
    for the hottest CPU core.
    """

    all_temp = psutil.sensors_temperatures()

    if platform.machine() == "x86_64":
        for cpu_temp in all_temp["coretemp"]:
            if cpu_temp.label == "Package id 0":
                cpu_current = cpu_temp.current

    elif platform.machine() == "aarch64":
        cpu_current = all_temp["cpu_thermal"][0].current

    return cpu_current

def ingest_elastic(cpu_current: int):
    """
    Upload temperature data to
    Elasticsearch.
    """

    es_client = elastic.connect_elasticsearch()

    if not es_client.indices.exists(index="temper-metric-data"):
        elastic.create_lifecycle_policy(es_client, "temper")
        elastic.create_index_template(es_client, "temper")
        es_client.indices.create_data_stream(name="temper")

    es_client.index(
        index="temper",
        document={
            "host": os.environ.get("HOSTNAME"),
            "cpu": cpu_current,
            "@timestamp": datetime.now(timezone.utc).strftime(constants.DATETIME_FORMAT)
        }
    )

    es_client.close()
