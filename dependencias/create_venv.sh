#!/bin/bash

python -m venv venv

source venv/bin/activate

python -m pip install --upgrade pip setuptools wheel

python -m pip install adafruit-circuitpython-dht

python -m pip install adafruit-circuitpython-bmp280

python -m pip install Flask