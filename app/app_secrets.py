import os, time
from os.path import join, dirname
from dotenv import load_dotenv
from flask import jsonify
import json

from sqlalchemy import create_engine, inspect

import decimal, datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


### SQLAlchemy config
#dbhost="mio1.serverafrica.net"
dbhost	        = os.environ.get("API_DB_HOST") 
dbname	        = os.environ.get("API_DB_NAME") 
dbuser	        = os.environ.get("API_DB_USER") 
pw	            = os.environ.get("API_DB_PASS")
flask_secret    = os.environ.get("API_FLASK_SECRET")
jwt_secret_key  = os.environ.get("JWT_SECRET_KEY")