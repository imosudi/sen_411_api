import os

#import graphene
from flask              import Flask, config
from flask_graphql      import GraphQLView
from flask_sqlalchemy   import SQLAlchemy
from flask_graphql_auth import GraphQLAuth
from flask_mail         import Mail
#from flask import g as ctx_stack

from .app_secrets import *

from flask_migrate import Migrate

app = Flask(__name__)

# app configs
app.config["JWT_SECRET_KEY"] = jwt_secret_key 
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 10  # 10 minutes
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 3  # 30 days

# Database configuration for mysql
app.config['SECRET_KEY'] = flask_secret
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{dbuser}:{pw}@{dbhost}/{dbname}" .format(dbuser=dbuser, pw=pw, dbhost=dbhost, dbname=dbname)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db          =SQLAlchemy(app)
migrate     = Migrate(app, db)
auth        = GraphQLAuth(app)
mail        = Mail(app)



from .                  import routes
from api.apiSchema      import *