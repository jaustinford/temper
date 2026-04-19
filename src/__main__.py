"""
Send out a constant stream
of temperature metric data to
Elasticsearch.
"""

import time

import tempcpu

def main():
    """
    While loop over method, sleeping
    in between intervals.
    """

    while True:
        # cpu_current = tempcpu.grab_hottest_core()
        # tempcpu.ingest_elastic(cpu_current)

        time.sleep(1000)

if __name__ == "__main__":
    main()
