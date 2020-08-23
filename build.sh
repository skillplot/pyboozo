#!/bin/bash

rm -r pyboozo.egg-info build dist
python setup.py bdist_wheel
