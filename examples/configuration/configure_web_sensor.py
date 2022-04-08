from sensor_api.web_sensor import WebSensor


def configure_sensors(sensors):
    '''! Create web wrapper for each sensor with additional information and converters 
    for the web api.

    @param sensors List of configured sensors
    @return wrappers List of sensor wrappers
    '''

    web_sensors = {}

    for sensor in sensors:
        # USB webcam
        if str(sensor) == 'webcam':
            def stream_converter(data):
                return b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + data + b'\r\n'

            web_sensors[str(sensor)] = WebSensor(sensor, 'image/jpeg',
                                                 'multipart/x-mixed-replace; boundary=frame', stream_converter)

        # Temperature Sensor (One-Wire Interface as System Resource)
        if str(sensor) == 'temp':
            def stream_converter(data):
                return f'data: {data} \n\n'

            web_sensors[str(sensor)] = WebSensor(
                sensor, 'application/json', 'text/event-stream', stream_converter)

    return web_sensors
