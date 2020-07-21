#!/bin/bash

cd /home/lbenedix/Fefefeed

pipenv run get_items
pipenv run generate_feed

