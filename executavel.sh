#!/bin/bash
sudo apt update
sudo apt install -y python3-pip
pip3 install numpy
python3 bancodados.py
python3 intancia.py
python3 webservice2.py 3