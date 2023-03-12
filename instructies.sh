#!/bin/bash
git clone git@github.com:jassummisko/NuTaalbot.git
pip3 install virtualenv
source venv/bin/activate
pip3 install -r requirements.txt
python3 main.py