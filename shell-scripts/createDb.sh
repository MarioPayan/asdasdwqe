#!/bin/bash
# This script prepares your environment for the first time creating the
# database for you, the virtualenv and puts your local_settings

# You are using postgresql, virtualenv and you have every requisite needed to
# work in your project

if [ "$#" -ne 7 ]; then
  echo 'Usage: '$0 'APP_NAME(Your application name)"' >&2
  exit 1
fi

APPNAME=$1
DBNAME=$2
USERNAME=$3
PASS=$4
SERVER=$5
CREATEVIRTUALENV=$6
INSTALLREQ=$7

if [ $CREATEVIRTUALENV != "false" ]; then
    echo 'CREANDO ENTORNO VIRTUAL...'
    virtualenv ~/.virtualenvs/$APPNAME
    . ~/.virtualenvs/$APPNAME/bin/activate
fi

if [ $INSTALLREQ != "false" ]; then
    echo 'INSTALANDO REQUERIMIENTOS...'
    pip install -r requirements.txt
    cp -r shell-scripts/menuware ~/.virtualenvs/$APPNAME/lib/python3.4/site-packages/
    cp -r shell-scripts/menuware ~/.virtualenvs/$APPNAME/lib/python3.5/site-packages/
fi

cd $APPNAME
PGPASSWORD=$PASS
psql -U $USERNAME -h $SERVER -p 5432 -c "CREATE DATABASE $DBNAME WITH OWNER $USERNAME"

echo 'Base de datos creada'