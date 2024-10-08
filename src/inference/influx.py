from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

INFLUX_ENDPOINT = "http://influxdb:8086"
INFLUX_ORG = "beg"
INFLUX_DATABASE = "inference_data_logs"
INFLUX_TOKEN = "influxadmintoken"

influx_client = InfluxDBClient(
    url=INFLUX_ENDPOINT,
    org=INFLUX_ORG,
    token=INFLUX_TOKEN,
)
influx_api = influx_client.write_api(write_options=SYNCHRONOUS)
