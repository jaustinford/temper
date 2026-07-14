"""
Send out a constant stream
of temperature metric data to
Elasticsearch.
"""

import os
import time
from datetime import datetime, timezone
import platform
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

    if constants.UNIT == "celsius":
        cpu_unit = cpu_current

    elif constants.UNIT == "fahrenheit":
        cpu_unit = (cpu_current * 9/5) + 32

    return cpu_unit

def main():
    """
    While loop over method, sleeping
    in between intervals.
    """

    while True:
        cpu_unit = grab_hottest_core()

        es_client = elastic.create_client("temper")

        elastic.upload_document(
            es_client,
            "temper",
            {
                "host": os.environ.get("HOST_HOSTNAME"),
                "cpu": cpu_unit,
                "unit": constants.UNIT,
                "@timestamp": datetime.now(timezone.utc).strftime(constants.DOC_FORMAT_TIMEDATE)
            }
        )

        es_client.close()

        time.sleep(constants.LOOP_INTERVAL)

if __name__ == "__main__":
    main()
