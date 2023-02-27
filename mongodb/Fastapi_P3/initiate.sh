#!/bin/bash

python3 pymongos.py 
uvicorn main:api --host 0.0.0.0

