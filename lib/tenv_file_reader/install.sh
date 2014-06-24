#!/usr/bin/env bash

# clean the current build
python3 setup.py clean --all

# build and install
python3 setup.py build
python3 setup.py install --user
