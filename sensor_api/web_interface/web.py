import flask

app = flask.Flask(__name__)

wrapper = None


@app.route('/get')
def handle_get():
    sensor_name = flask.request.args.get('sensor', '')
    if len(sensor_name) > 0 and sensor_name in wrapper:
        data = wrapper[sensor_name].sensor.get_data_safe()
        return flask.Response(data, mimetype=wrapper[sensor_name].data_type)

    return flask.Response('Request is not valid')


@app.route('/stream')
def handle_stream():
    sensor_name = flask.request.args.get('sensor', '')
    if len(sensor_name) > 0 and sensor_name in wrapper:

        def generator():
            while True:
                data = wrapper[sensor_name].sensor.get_data_safe()
                yield wrapper[sensor_name].stream_converter(data)

        return flask.Response(generator(), mimetype=wrapper[sensor_name].stream_type)

    return flask.Response('Request is not valid')


@app.route('/')
def handle_index():
    return flask.render_template('index.html', sensors=list(wrapper.keys()))


def start_app(new_wrapper: dict) -> None:
    global wrapper
    wrapper = new_wrapper

    app.run(threaded=True, host='0.0.0.0', port=8080, debug=True, use_reloader=False)
