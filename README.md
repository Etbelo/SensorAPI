# SensorAPI

Simple sensor api based on flask for getting and streaming data from web interface to be embedded in other website or access using the terminal. Based on custom asynchronous sensor library for concurrent access to resources by multiple threads.

## Setup

* Editable local installation

```shell
pip3 install -e .
```

## Examples

### Without Authentication

* Start

```shell
make run -C examples/auth_none
```

* Access Resource

```shell
curl "<host>:<port>/get?sensor=webcam" --output "test.jpg"
```

### URL Token Authentication

* Store token as environment variable

* Start

```shell
make run -C examples/auth_url
```

* Access Resource

```shell
curl "<host>:<port>/get?sensor=webcam&token=<api_token>" --output "test.jpg"
```
