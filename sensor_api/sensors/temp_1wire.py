import json
import re

from sensor_api.sensors.sensor import Sensor


class Temp1Wire(Sensor):
    '''! Temperature sensor generator for registered one-wire temperature sensors.
    Raw data is returned in JSON format.
    '''

    def __init__(self):
        '''! Construct a new temp sensor generator object.
        @param id Data generator id and packet identifier
        '''
        super().__init__('temp_1wire', 'json')

        self.sensor_files = ['/sys/bus/w1/devices/28-0620179e2c49/w1_slave',
                             '/sys/bus/w1/devices/28-062017b40914/w1_slave',
                             '/sys/bus/w1/devices/28-0120506f5efe/w1_slave']

        self.valid = self.test_sensor()

    def read_one_wire(self, sensor_file) -> float:
        '''! Open local one-wire sensor file and retrieve its data.
        @param sensor_file Path to sensor file
        @return Temperature as floating point number
        '''

        try:
            with open(sensor_file) as sensor:
                sensor_result = re.search('t=(\d+)', sensor.read())

                if sensor_result is not None:
                    return int(sensor_result.group(1)) / 1000.0
        except:
            pass

        return None

    def get_data(self) -> str:
        '''! Retrieve temperature data of all registered sensors in JSON format.
        @return Data as python dictionary
        '''

        data = {}

        for i in range(len(self.sensor_files)):
            value = self.read_one_wire(self.sensor_files[i])
            data[f'sensor_{i}'] = value

        return json.dumps(data)

    def test_sensor(self) -> bool:
        '''! Test if data is retrieved from all sensors.
        @return True if generator is active
        '''

        data = self.get_data()
        data_dict = json.loads(data)

        success = True

        for sensor in data_dict:
            success &= isinstance(data_dict[sensor], float)

        return success

    def dump_file(self) -> None:
        '''! Retrieve temperature data of all registered sensors and saving them 
        as a file.
        '''

        data = self.get_data()

        try:
            with open(self.get_filename(), 'w') as file:
                json.dump(data, file)
        except:
            pass
