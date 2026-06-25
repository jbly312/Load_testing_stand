import os
from locust import events
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

INFLUX_URL = os.environ.get('INFLUX_URL', 'http://localhost:8086')
INFLUX_TOKEN = os.environ.get('INFLUX_TOKEN', 'my-super-secret-token')
INFLUX_ORG = os.environ.get('INFLUX_ORG', 'loadtest')
INFLUX_BUCKET = os.environ.get('INFLUX_BUCKET', 'locust')

_client = None
_write_api = None

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    global _client, _write_api
    _client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
    _write_api = _client.write_api(write_options=SYNCHRONOUS)
    print(f"influxdb listener - {INFLUX_URL} (bucket={INFLUX_BUCKET})")

@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, **kwargs):

    if _write_api is None:
        return

    point = (
        Point("requests")
        .tag("name", name)
        .tag("method", request_type)
        .tag("success", "false" if exception else "true")
        .field("response_time", float(response_time))
    )
    try:
        _write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG,record=point)
    except Exception as e:
        print(f"failed writing to influxdb: {e}"
              )

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    global _client
    if _client:
        _client.close()