#!/bin/bash

python crawl_tapology_events.py
python parse_tapology_events_fighters-step1.py
python crawl_tapology_fighters.py
python parse_tapology_events_fighters-step2.py
python parse_tapology_events_fighters_fights.py