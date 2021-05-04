#!/bin/bash
if [ ! -d "env" ]; then
  python3.9 -m venv env
  if [ $? != 0 ]; then exit 1; fi
fi

source ./env/bin/activate && python3.9 -m pip install -r requirements.txt
if [ $? != 0 ]; then exit 1; fi
