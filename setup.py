from setuptools import setup

setup(
    name='sensor_api',
    description='Sensor web interface for data request and streaming.',
    project_urls={
        'GitHub': 'https://github.com/Etbelo/SensorAPI'
    },
    license='MIT',
    author='Johann Erhard',
    zip_safe=False,
    install_requires=[
        'Flask',
        'Flask_Cors',
        'Flask-HTTPAuth',
        'sensor_async@git+https://github.com/Etbelo/SensorAsync.git#egg=sensor_async',
        'Werkzeug'
    ]
)
