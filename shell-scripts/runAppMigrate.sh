#!/bin/bash

APPNAME=$1
SETTINGS=$2

. ~/.virtualenvs/$APPNAME/bin/activate

python manage.py makemigrations --settings=config.settings.$SETTINGS
python manage.py migrate --settings=config.settings.$SETTINGS
