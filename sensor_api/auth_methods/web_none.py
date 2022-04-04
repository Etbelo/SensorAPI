import flask
from flask_cors import cross_origin

import sensor_api.api_methods as API


app = flask.Flask(__name__, template_folder='../templates')


@app.route('/get')
@cross_origin()
def handle_get():
    '''! Return data to the user once
    '''

    return API.get()


@app.route('/stream')
@cross_origin()
def handle_stream():
    '''! Stream data to the user as long as requested
    '''

    return API.stream()


@app.route('/')
def handle_index():
    ''' Show list of configured sensors and data links
    '''

    return API.index()


def start_app(port: int, wrappers: dict) -> None:
    API.wrappers = wrappers
    app.run(threaded=True, host='0.0.0.0', port=port, debug=False, use_reloader=False)
