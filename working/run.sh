#!/bin/bash
find json-output/ -name "*.json" | parallel -j 8 python3 "/home/joel/Documents/norsand/simulation/main.py" -i {}
