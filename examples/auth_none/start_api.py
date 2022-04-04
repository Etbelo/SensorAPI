import argparse

from sensor_api.web_wrapper import WebWrapper
from sensor_api.auth_methods.web_none import start_app

import sensor_async.info as SENSOR_INFO


def get_wrappers(sensors):
    '''! Create web wrapper for each sensor with additional information and converters 
    for the web api.

    @param sensors List of configured sensors
    @return wrappers List of sensor wrappers
    '''

    wrappers = {}

    for sensor in sensors:
        # USB webcam
        if str(sensor) == 'webcam':
            def stream_converter(data):
                return b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + data + b'\r\n'

            wrappers[str(sensor)] = WebWrapper(sensor, 'image/jpeg',
                                               'multipart/x-mixed-replace; boundary=frame', stream_converter)

        # Temperature Sensor (One-Wire Interface as System Resource)
        if str(sensor) == 'temp':
            def stream_converter(data):
                return f'data: {data} \n\n'

            wrappers[str(sensor)] = WebWrapper(
                sensor, 'application/json', 'text/event-stream', stream_converter)

    return wrappers


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', metavar='CONFIG', type=str, help='Sensor config file')
    parser.add_argument('-p', metavar='PORT', type=int, help='Local webserver port')

    args = parser.parse_args()

    sensors = SENSOR_INFO.sensors_from_config(args.c)
    wrappers = get_wrappers(sensors)

    print('Start app using no authentication')
    print(f'Configured sensors: {list(wrappers.keys())}')

    start_app(args.p, wrappers)
