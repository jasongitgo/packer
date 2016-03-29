#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, request

from app import App, db
from app.components.main import main
from manage import app


@main.route('/')
def home():
    return app.send_static_file('home.html')

