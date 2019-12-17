#!/bin/bash
export DICTPLUS_VER=$(cat version.json | grep "version" | sed 's/ "version": "//g' | sed 's/"//g' | awk '{$1=$1};1')
echo "Generating Docs for version '$DICTPLUS_VER'"
cd docs
sphinx-apidoc -o source ../dict_plus -f
make html
