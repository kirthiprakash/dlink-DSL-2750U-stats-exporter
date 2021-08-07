from prometheus_client import start_http_server
from prometheus_client.core import GaugeMetricFamily, REGISTRY
import random
import time
from scrapper.scarpe import Scrape

class DlinkCollector(object):
    def collect(self):
        bytes_sent, bytes_received = Scrape()
        rx_bytes = GaugeMetricFamily('lan_nw_receive_bytes', 'RB', labels=['device'])
        rx_bytes.add_metric(['bar'], bytes_received)
        yield rx_bytes

if __name__ == '__main__':
    REGISTRY.register(DlinkCollector())
    # Start up the server to expose the metrics.
    start_http_server(8001)

# Go to sleep until Ctrl+C!
try:
    wait_time = 20.0
    while True:
        time.sleep(wait_time)
except KeyboardInterrupt:
    pass


