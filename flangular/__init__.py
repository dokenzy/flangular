# -*- coding: utf-8 -*-

from mongoengine import connect

import flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.restful import Api

from . import config

app = flask.Flask(__name__)
app.config.from_object(config)
connect(app.config['MONGODB_DB'])
db = MongoEngine(app)
api = Api(app)

from . import core
from . import user
from . import computer

#db.create_all()

# Create admim user if not exists
user.User.new_user('admin@flangular.js', 'admin')
