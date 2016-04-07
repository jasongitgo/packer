#! /usr/bin/env python
# -*- coding: utf-8 -*-

from config import config
from flask import Flask
from flask.ext.compress import Compress
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
compress = Compress()
db = SQLAlchemy()
from app.models import App, Moudle



def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    login_manager.init_app(app)
    compress.init_app(app)
    db.init_app(app)
    return app
