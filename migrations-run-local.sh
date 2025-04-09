#!/bin/sh
 
FLASK_ENV=dev DATABASE_URL=sqlite:///data.db flask db migrate
FLASK_ENV=dev DATABASE_URL=sqlite:///data.db flask db upgrade
