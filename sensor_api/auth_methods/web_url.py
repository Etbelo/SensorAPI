from functools import wraps

import flask
from flask_cors import cross_origin

import sensor_api.api_methods as API


app = flask.Flask(__name__, template_folder='../templates')
tokens_ = []


def token_required(f):
    '''! Decorator for verifying the user specified api token
    '''

    @wraps(f)
    def decorated(*args, **kwargs):
        token = flask.request.args.get('token', '')

        if len(token) > 0 and token in tokens_:
            return f(*args, **kwargs)

        return 'Unauthorized Access!', 401

    return decorated


@app.route('/get')
@cross_origin()
@token_required
def handle_get():
    '''! Return data to the user once
    '''

    return API.get()


@app.route('/stream')
@cross_origin()
@token_required
def handle_stream():
    '''! Stream data to the user as long as requested
    '''

    return API.stream()


@app.route('/')
@token_required
def handle_index():
    ''' Show list of configured sensors and data links
    '''

    return API.index()


def start_app(port: int, wrappers: dict, tokens: list) -> None:
    global tokens_
    tokens_ = tokens

    API.wrappers = wrappers
    app.run(threaded=True, host='0.0.0.0', port=port, debug=False, use_reloader=False)
