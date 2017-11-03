#!/bin/bash
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
#find $(dirname $0) | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf