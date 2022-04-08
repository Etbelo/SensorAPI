# SensorAPI

Simple sensor api based on flask for getting and streaming data from web interface to be embedded in other website or access using the terminal. Based on custom asynchronous sensor library for concurrent access to resources by multiple threads.

## Setup

* Editable local installation

```shell
pip3 install -e .
```

## Examples

Webcam streaming with automatic asynchronous data access hanlding. Ensures full framerate for webstreaming when multiple clients access the same stream. Webcam and other sensors can be configured in the config.yaml file as defined in [SensorAsync](https://github.com/Etbelo/SensorAsync) library.

### Without Authentication

* Start app 

```shell
make run-none -C examples/
```

* Access sensor using terminal or webbrowser

```shell
curl "<host>:<port>/get?sensor=webcam" --output "test.jpg"
```

### URL Token Authentication

* Store token as environment variable

* Start

```shell
make run-url-token -C examples/
```

* Access sensor using terminal or webbrowser

```shell
curl "<host>:<port>/get?sensor=webcam&token=<api_token>" --output "test.jpg"
```
