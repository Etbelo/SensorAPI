from dataclasses import dataclass
from typing import Callable

from sensor_api.sensors.sensor import Sensor


@dataclass
class SensorWrapper:
    '''! Sensor wrapper for web usage. Contains sensor and additional information
    and functionality for web interface, i.g., content types and response converters.
    '''

    sensor: Sensor
    mimetype: str
    mimetype_stream: str
    stream_converter: Callable

    def get_response(self):
        '''! Get normal http response

        @return Datatype dependent of sensor type
        '''

        return self.sensor.get_data_safe()

    def get_stream_response(self):
        '''! Get stream http response using stream_converter

        @return Datatype dependent of sensor type and stream_converter
        '''

        data = self.sensor.get_data_safe()
        return self.stream_converter(data)
