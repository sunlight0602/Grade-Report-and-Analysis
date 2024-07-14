#!/bin/bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src

echo "Enter run_main.sh"

# get mariadb pre-requisites
apt-get update -y
apt-get install -y libmariadb-dev
apt-get install -y gcc
pip3 install mariadb

# get vim
apt-get install vim

python3 ./src/main.py