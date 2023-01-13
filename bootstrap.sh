#!/bin/sh
export FLASK_APP=run.py
pipenv run flask --debug run -h 0.0.0.0