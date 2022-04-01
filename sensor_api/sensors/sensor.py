import abc
import os
import datetime
import threading


class Sensor(abc.ABC):
    '''! Provides basic structure of a sensor and its necessary functions.
    Some functions are already implemented.
    '''

    def __init__(self, name: str, file_extension: str) -> None:
        '''! Construct a new sensor object.

        @param name Data generator name and command identifier
        @param id Data generator id and packet identifier
        @param type Generator datatype
        '''

        super().__init__()

        # arguments
        self.name = name
        self.file_extension = file_extension

        # variables
        self.reading = False
        self.data = None
        self.mutex = threading.Condition()
        self.valid = False

    def __str__(self) -> str:
        '''! String identifier of this sensor

        @return Sensor name
        '''

        return self.name

    def get_filename(self, base_path: str, delta_hours: int = 1) -> str:
        '''! Construct file name for a single data measurement

        @param base_path Base file path
        @param delta_hours Time shift added to UTC
        @return File name
        '''

        timestamp = (datetime.datetime.now() +
                     datetime.timedelta(hours=delta_hours)).strftime('%Y%m%d-%H%M%S')

        filename = f'data_{self.name}_{timestamp}.{self.file_extension}'

        return os.path.join(base_path, filename)

    def get_data_safe(self):
        '''! Retrieve a single measurement in default data format by additionally
        handling the access of multiple threads.

        @return Data in format dependent to sensor
        '''

        if not self.reading:
            # Actively read data from resource
            self.reading = True
            self.data = self.get_data()

            # Notify all threads that wait for data
            with self.mutex:
                self.mutex.notify_all()

            self.reading = False
        else:
            # Other thread is reading right now: Wait to be notified
            with self.mutex:
                self.mutex.wait()

        # Return data
        return self.data

    @abc.abstractmethod
    def get_data(self):
        '''! Retrieve a single measurement in default data format.

        @return Data in format dependent to sensor
        '''

        pass

    @abc.abstractmethod
    def test_sensor(self) -> bool:
        '''! Test if the sensor returns valid data

        @return True if the sensor is valid
        '''

        pass

    @abc.abstractmethod
    def dump_file(self, base_path: str) -> None:
        '''! Store a single measurement as a file

        @param base_path File base path
        '''

        pass
