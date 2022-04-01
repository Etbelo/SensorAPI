class SensorWrapper:

    def __init__(self, sensor, data_type, stream_type, stream_converter) -> None:

        self.sensor = sensor
        self.data_type = data_type
        self.stream_type = stream_type
        self.stream_converter = stream_converter
