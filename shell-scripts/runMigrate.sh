#!/bin/bash
# This script prepares your environment for the first time creating the
# database for you, the virtualenv and puts your local_settings

# You are using postgresql, virtualenv and you have every requisite needed to
# work in your project

if [ "$#" -ne 4 ]; then
  echo 'Usage: '$0 'APP_NAME(Your application name)"' >&2
  exit 1
fi

APPNAME=$1
SETTINGS=$2
CREATEVIRTUALENV=$3
INSTALLREQ=$4

if [ $CREATEVIRTUALENV != "false" ]; then
    echo 'CREANDO ENTORNO VIRTUAL...'
    virtualenv ~/.virtualenvs/$APPNAME
    source ~/.virtualenvs/$APPNAME/bin/activate
fi

if [ $INSTALLREQ != "false" ]; then
    echo 'INSTALANDO REQUERIMIENTOS...'
    pip install -r requirements.txt
    cp -r shell-scripts/menuware ~/.virtualenvs/$APPNAME/lib/python3.4/site-packages/
    cp -r shell-scripts/menuware ~/.virtualenvs/$APPNAME/lib/python3.5/site-packages/
fi

cd $APPNAME

echo 'CORRIENDO MAKEMIGRATIONS...'
python manage.py makemigrations --settings=config.settings.$SETTINGS
echo 'CORRIENDO MIGRATE...'
python manage.py migrate --settings=config.settings.$SETTINGS
python manage.py migrate --database=logs --settings=config.settings.$SETTINGS
echo 'CORRIENDO SCRIPT DE CONFIGURACIÓN INICIAL...'
python manage.py shell < script.py --settings=config.settings.$SETTINGS
echo 'CORRIENDO SERVIDOR...'
python manage.py runserver --settings=config.settings.$SETTINGS
