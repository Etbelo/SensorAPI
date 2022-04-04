import os

from sensor_api.web_wrapper import WebWrapper
from sensor_api.auth_methods.web_none import start_app

import sensor_async.info as SENSOR_INFO


def get_wrappers(sensors):
    wrappers = {}

    for sensor in sensors:
        if str(sensor) == 'webcam':
            def stream_converter(data):
                return b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + data + b'\r\n'

            wrappers[str(sensor)] = WebWrapper(sensor, 'image/jpeg',
                                               'multipart/x-mixed-replace; boundary=frame', stream_converter)

        if str(sensor) == 'temp':
            def stream_converter(data):
                return f'data: {data} \n\n'

            wrappers[str(sensor)] = WebWrapper(
                sensor, 'application/json', 'text/event-stream', stream_converter)

    return wrappers


if __name__ == '__main__':
    sensors = SENSOR_INFO.sensors_from_config('config.yaml')
    wrappers = get_wrappers(sensors)

    start_app(5000, wrappers)
