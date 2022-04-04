import flask
from flask_cors import cross_origin
from flask_httpauth import HTTPTokenAuth

import sensor_api.api_methods as API


app = flask.Flask(__name__, template_folder='../templates')
auth = HTTPTokenAuth()
tokens_ = []


@auth.verify_token
def verify_token(token):
    if token in tokens_:
        return tokens_[token]


@app.route('/get')
@cross_origin()
@auth.login_required
def handle_get():
    '''! Return data to the user once
    '''

    return API.get()


@app.route('/stream')
@cross_origin()
@auth.login_required
def handle_stream():
    '''! Stream data to the user as long as requested
    '''

    return API.stream()


@app.route('/')
@auth.login_required
def handle_index():
    ''' Show list of configured sensors and data links
    '''

    return API.index()


def start_app(port: int, wrappers: dict, tokens: list) -> None:
    global tokens_
    tokens_ = tokens

    API.wrappers = wrappers
    app.run(threaded=True, host='0.0.0.0', port=port, debug=False, use_reloader=False)
