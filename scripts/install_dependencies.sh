#!/usr/bin/env bash

cd /home/ubuntu/disco_bot/

python3.10 -m venv .venv

.venv/bin/activate

pip install -U setuptools pip
pip install -r requirements.txt
