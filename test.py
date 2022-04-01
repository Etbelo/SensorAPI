import threading

from sensor_api.sensors.usb_cam import USBCam


def read_data(sensor):
    data = sensor.get_data_safe()
    print(len(data))


if __name__ == '__main__':

    cam = USBCam(video_source=1)

    # t0 = threading.Thread(target=read_data, args=(cam,), daemon=True)
    # t1 = threading.Thread(target=read_data, args=(cam,), daemon=True)

    # t0.start()
    # t1.start()

    # t0.join()
    # t1.join()
