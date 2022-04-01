import flask
from flask_cors import cross_origin
from functools import wraps

app = flask.Flask(__name__)

wrappers_ = None
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
@token_required
@cross_origin('')
def handle_get():
    '''! Return data to the user once
    '''

    sensor_name = flask.request.args.get('sensor', '')
    if len(sensor_name) > 0 and sensor_name in wrappers_:
        return flask.Response(
            wrappers_[sensor_name].get_response(),
            mimetype=wrappers_[sensor_name].mimetype)

    return flask.Response('Request is not valid')


@app.route('/stream')
@token_required
@cross_origin()
def handle_stream():
    '''! Stream data to the user as long as requested
    '''

    sensor_name = flask.request.args.get('sensor', '')
    if len(sensor_name) > 0 and sensor_name in wrappers_:

        def generator():
            while True:
                yield wrappers_[sensor_name].get_stream_response()

        return flask.Response(generator(),
                              mimetype=wrappers_[sensor_name].mimetype_stream)

    return flask.Response('Request is not valid')


@app.route('/')
@token_required
def handle_index():
    ''' Show list of configured sensors and data links
    '''

    return flask.render_template('index.html', sensors=list(wrappers_.keys()))


def start_app(port: int, wrappers: dict, tokens: list) -> None:
    global wrappers_, tokens_
    wrappers_ = wrappers
    tokens_ = tokens

    app.run(threaded=True, host='0.0.0.0', port=port, debug=False, use_reloader=False)
