import argparse
import yaml
import os

from sensor_api.web_interface.web import start_app
from sensor_api.web_interface.sensor_wrapper import SensorWrapper

from sensor_api.sensors.usb_cam import USBCam
from sensor_api.sensors.temp_1wire import Temp1Wire


def read_config(config_file):
    '''! Read yaml config file

    @return Config dictionary
    '''

    try:
        with open(config_file, 'rb') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(e)

    return None


def configure_sensor(wrappers, name, config):
    '''! Configure sensor using config and additional web parameters

    @param wrappers List of already configured wrappers
    @param name Name of sensor as configured in config file
    @param config Config dictionary of sensor
    @return wrappers New list of wrappers
    '''

    if name == 'usb_cam':
        sensor = USBCam(config['video_source'], config['resolution'])

        if sensor is not None and sensor.valid:

            def stream_converter(data):
                return b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + data + b'\r\n'

            wrappers[str(sensor)] = SensorWrapper(sensor, 'image/jpeg',
                                                  'multipart/x-mixed-replace; boundary=frame', stream_converter)

    if name == 'temp_1wire':
        sensor = Temp1Wire()

        if sensor is not None and sensor.valid:

            def stream_converter(data):
                return f'data: {data} \n\n'

            wrappers[str(sensor)] = SensorWrapper(
                sensor, 'application/json', 'text/event-stream', stream_converter)

    return wrappers


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', metavar='CONFIG', required=True, type=str,
                        help='Path to config file for sensor configuration')
    parser.add_argument('-p', metavar='PORT', required=False, type=int, default=8080,
                        help='Port for flask web application')
    args = parser.parse_args()

    # Read config file
    config = read_config(args.c)

    if config is not None:
        # Configure and test sensors for web usage
        wrappers = {}

        for sensor_name in config:
            try:
                if config[sensor_name]['enable']:
                    wrappers = configure_sensor(wrappers, sensor_name, config[sensor_name])
            except Exception as e:
                print(e)

        # Register API tokens
        api_tokens = []
        api_tokens.append(os.getenv('API_TOKEN'))

        if len(wrappers) > 0:
            print(f'Configured sensors: {list(wrappers.keys())}')

            # Start flask application
            start_app(args.p, wrappers, api_tokens)
