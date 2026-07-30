#!/bin/bash
/usr/bin/python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install numpy==2.5 scipy==1.18
pip install -e .
echo "Done!"
