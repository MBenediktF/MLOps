from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv
import os

load_dotenv()

influx_endpoint = "http://influxdb:8086"
influx_org = os.getenv('INFLUX_ORG')
influx_database = os.getenv('INFLUX_DATABASE')
influx_token = os.getenv('INFLUX_TOKEN')

influx_client = InfluxDBClient(
    url=influx_endpoint,
    org=influx_org,
    token=influx_token,
)
influx_api = influx_client.write_api(write_options=SYNCHRONOUS)

DEFAULT_COLUMNS = ["feature_file_url", "sensor_value", "prediction"]


def enable_local_dev(influx_endpoint_local):
    global influx_client
    global influx_api
    influx_client.close()
    influx_client = InfluxDBClient(
        url=influx_endpoint_local,
        org=influx_org,
        token=influx_token,
    )
    influx_api = influx_client.write_api(write_options=SYNCHRONOUS)


def write_record(record):
    influx_api.write(
        bucket=influx_database,
        org=influx_org,
        record=record)


def fetch_records(measurement, columns=DEFAULT_COLUMNS):
    columns_string = ', '.join(f'"{col}"' for col in columns)
    query = f'''
    from(bucket: "{influx_database}")
    |> range(start: -1y)
    |> filter(fn: (r) => r._measurement == "{measurement}")
    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    |> keep(columns: [{columns_string}])
    '''
    result = influx_client.query_api().query(query)
    records = []
    for table in result:
        for record in table.records:
            # remove unnecessary datapoints
            record.values.pop('result', None)
            record.values.pop('table', None)
            records.append(record.values)
    return records


def count_records(measurement):
    query = f'''
    from(bucket: "{influx_database}")
    |> range(start: -1y)
    |> filter(fn: (r) => r._measurement == "{measurement}")
    |> filter(fn: (r) => r._field == "feature_file_url")
    |> count()
    '''
    result = influx_client.query_api().query(query)
    count = 0
    for table in result:
        for record in table.records:
            count += record.get_value()
    return count


def create_record(measurement):
    return Point(measurement)
