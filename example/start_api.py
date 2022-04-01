import yaml

from sensor_api.web_interface.web import start_app
from sensor_api.web_interface.sensor_wrapper import SensorWrapper

from sensor_api.sensors.usb_cam import USBCam
from sensor_api.sensors.temp_1wire import Temp1Wire


def read_config(config_file):
    try:
        with open(config_file, 'rb') as file:
            return yaml.safe_load(file)
    except:
        pass

    return None


def configure_sensor(wrapper, name, config):

    if name == 'usb_cam':
        sensor = USBCam(config['video_source'], config['resolution'])

        if sensor is not None and sensor.valid:

            def stream_converter(data):
                return b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + data + b'\r\n'

            wrapper[str(sensor)] = SensorWrapper(sensor, 'image/jpeg',
                                                 'multipart/x-mixed-replace; boundary=frame', stream_converter)

    if name == 'temp_1wire':
        sensor = Temp1Wire()

        if sensor is not None and sensor.valid:

            def stream_converter(data):
                return f'data: {data} \n\n'

            wrapper[str(sensor)] = SensorWrapper(
                sensor, 'application/json', 'text/event-stream', stream_converter)

    return wrapper


if __name__ == '__main__':

    config = read_config('config.yaml')

    wrapper = {}

    for sensor_name in config:
        try:
            if config[sensor_name]['enable']:
                wrapper = configure_sensor(wrapper, sensor_name, config[sensor_name])
        except Exception as e:
            print(e)

    print(f'Configured sensors: {list(wrapper.keys())}')

    start_app(wrapper)
