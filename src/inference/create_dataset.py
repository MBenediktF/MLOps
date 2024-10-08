# Read the data from influx and s3 in order to create a new dataset
# with features and labels fron an measuerment

import boto3
from influxdb_client import InfluxDBClient
from log_message import log_message


S3_ENDPOINT = "http://minio:9000"
S3_ACCESS_KEY_ID = "minioadmin"
S3_SECRET_ACCESS_KEY = "minioadminpassword"
BUCKET_NAME = "mlops-research"

INFLUX_ENDPOINT = "http://influxdb:8086"
INFLUX_ORG = "beg"
INFLUX_DATABASE = "inference_data_logs"
INFLUX_TOKEN = "influxadmintoken"

s3_client = boto3.client(
    's3',
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY_ID,
    aws_secret_access_key=S3_SECRET_ACCESS_KEY
)


def create_dataset_from_measurement(measurement):
    # fetch datapoints from influx
    measurement = fetch_measurement(measurement,
                                    columns=["feature_file_url",
                                             "sensor_value"])

    # read images from s3
    

    # create iage metadata string

    # save images
    return


def fetch_measurement(measurement,
                      columns=["feature_file_url",
                               "sensor_value",
                               "prediction"]):
    columns_string = ', '.join(f'"{col}"' for col in columns)
    query = f'''
    from(bucket: "{INFLUX_DATABASE}")
    |> range(start: -1y)
    |> filter(fn: (r) => r._measurement == "{measurement}")
    |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
    |> keep(columns: [{columns_string}])
    '''

    with InfluxDBClient(url=INFLUX_ENDPOINT,
                        token=INFLUX_TOKEN,
                        org=INFLUX_ORG) as client:
        result = client.query_api().query(query)
        records = []
        for table in result:
            for record in table.records:
                # remove unnecessary datapoints
                record.values.pop('result', None)
                record.values.pop('table', None)
                records.append(record.values)
        return records
