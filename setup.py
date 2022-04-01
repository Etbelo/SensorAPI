from setuptools import setup

setup(
    name='sensor_api',
    description='Sensor classes and web interface for web access and streaming.',
    author='Johann Erhard',
    zip_safe=False,
    install_requires=[
        'opencv_python',
        'PyTurboJPEG',
        'Flask',
        'flask-cors'
        'v4l2py',
    ]
)
