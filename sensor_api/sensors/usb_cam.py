import enum
import platform

from sensor_api.sensors.sensor import Sensor

if platform.system() == 'Linux':
    import v4l2py

import cv2
import turbojpeg


class USBCam(Sensor):
    '''! Handles image reader for usb camera resources using OpenCV or
    Video4Linux drivers.
    '''

    class Type(enum.Enum):
        '''! Driver type'''

        OpenCV = 1
        V4L = 2

    def __init__(
            self, video_source: int = 0, resolution: tuple = (1080, 720),
            type: Type = None) -> None:
        '''! Construct a new USBCam object 

        @param id Data generator id and packet identifier
        @param video_source Local camera source id
        @param resolution Camera resolution for reading
        @param type Image generator reading type
        '''

        super().__init__('usb_cam', 'jpg')

        self.video_source = video_source
        self.resolution = resolution
        self.type = type

        # Automatic type selection
        if platform.system() == 'Windows':
            self.type = USBCam.Type.OpenCV

        if type == None and platform.system() == 'Linux':
            self.type = USBCam.Type.V4L

        # Setup capture device for different types
        try:
            if self.type == USBCam.Type.OpenCV:
                self.video_cap = cv2.VideoCapture(video_source)
                self.video_cap.set(cv2.CAP_PROP_FOURCC, 0x47504A4D)
                self.video_cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
                self.video_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
                self.encoder = turbojpeg.TurboJPEG()

            if self.type == USBCam.Type.V4L:
                device = v4l2py.Device.from_id(video_source)
                device.video_capture.set_format(
                    resolution[0], resolution[1], 'MJPG')
                self.video_cap = iter(device)

            self.valid = self.test_sensor()
        except:
            pass

    def get_data(self) -> bytes:
        '''! Retrieve image data in encoded jpg format

        @return Data in bytes
        '''

        data = bytearray()

        try:
            if self.type == USBCam.Type.OpenCV:
                frame = self.video_cap.read()[1]
                data = self.encoder.encode(frame)

            if self.type == USBCam.Type.V4L:
                data = next(self.video_cap)
        except:
            pass

        return data

    def test_sensor(self) -> bool:
        '''! Test if the sensor returns valid data

        @return True if USBCam is valid
        '''

        data = self.get_data()

        return len(data) > 0

    def dump_file(self, base_path: str = '') -> None:
        '''! Store a single image as a file

        @param base_path File base path
        '''

        data = self.get_data()

        try:
            with open(self.get_filename(base_path), 'wb') as file:
                file.write(data)
        except:
            pass
