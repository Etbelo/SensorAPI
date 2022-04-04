import flask

wrappers = None


def get():
    '''! Return data to the user once

    @return Flask response
    '''

    sensor_name = flask.request.args.get('sensor', '')
    if len(sensor_name) > 0 and sensor_name in wrappers:
        return flask.Response(
            wrappers[sensor_name].get_response(),
            mimetype=wrappers[sensor_name].mimetype)

    return flask.Response('Request is not valid', status=400)


def stream():
    '''! Stream data to the user as long as requested 

    @return Flask response
    '''

    sensor_name = flask.request.args.get('sensor', '')
    if len(sensor_name) > 0 and sensor_name in wrappers:

        def generator():
            while True:
                yield wrappers[sensor_name].get_stream_response()

        return flask.Response(generator(),
                              mimetype=wrappers[sensor_name].mimetype_stream)

    return flask.Response('Request is not valid', status=400)


def index():
    '''! Show list of configured sensors and data links

    @return Flask response
    '''

    return flask.render_template('index.html', sensors=list(wrappers.keys()))
