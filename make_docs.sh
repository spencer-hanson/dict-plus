#!/bin/bash
export VERSION_JSON_PATH=$(pwd)/version.json
cd docs
sphinx-apidoc -o source ../dict_plus -f
make html
