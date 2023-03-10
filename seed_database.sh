#!/bin/bash

rm db.sqlite3
rm -rf ./avengersassembleapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations avengersassembleapi
python3 manage.py migrate avengersassembleapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata comic
python3 manage.py loaddata movie
python3 manage.py loaddata avengeruser
python3 manage.py loaddata character
python3 manage.py loaddata userteam
python3 manage.py loaddata battle
python3 manage.py loaddata vote
python3 manage.py loaddata cart