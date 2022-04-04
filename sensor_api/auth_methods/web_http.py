import flask
from flask_cors import cross_origin
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

import sensor_api.api_methods as API


app = flask.Flask(__name__, template_folder='../templates')
auth = HTTPBasicAuth()
users_ = {}


@auth.verify_password
def verify_password(username, password):
    if username in users_ and \
            check_password_hash(users_.get(username), password):
        return username


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


def start_app(port: int, wrappers: dict, users: dict) -> None:
    global users_
    users_ = users

    API.wrappers = wrappers
    app.run(threaded=True, host='0.0.0.0', port=port, debug=False, use_reloader=False)
