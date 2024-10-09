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

DEFAULT_COLUMNS = ["feature_file_url", "sensor_value", "prediction"]


def write_record(record):
    influx_api.write(
        bucket=INFLUX_DATABASE,
        org=INFLUX_ORG,
        record=record)


def fetch_records(measurement, columns=DEFAULT_COLUMNS):
    columns_string = ', '.join(f'"{col}"' for col in columns)
    query = f'''
    from(bucket: "{INFLUX_DATABASE}")
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


def create_record(measurement):
    return Point(measurement)
