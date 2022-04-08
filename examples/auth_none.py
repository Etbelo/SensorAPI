import argparse

from sensor_api.auth_methods.web_none import start_app
import sensor_async.info as SENSOR_INFO

from configuration.configure_web_sensor import configure_sensors


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', metavar='CONFIG', type=str, help='Sensor config file')
    parser.add_argument('-p', metavar='PORT', type=int, help='Local webserver port')

    args = parser.parse_args()

    sensors = SENSOR_INFO.get_sensors_from_config(args.c)
    web_sensors = configure_sensors(sensors)

    print('Start app using no authentication')
    print(f'Configured sensors: {list(web_sensors.keys())}')

    start_app(args.p, web_sensors)
