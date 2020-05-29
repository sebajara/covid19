#!/bin/bash
python3 covidtracking_update.py
python3 nytimes_updatedata.py
rm ecdc/ecdc_data.csv
python3 ecdc_update.py
