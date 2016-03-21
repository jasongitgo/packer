#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, request

from app import App, db
from app.components.main import main
from manage import app


@main.route('/')
def home():
    print 111111
    return app.send_static_file('home.html')


@main.route('/app/new', methods=['GET', 'POST'])
def app_new():
    print request.json
    print request.json['name']
    app = App(name=request.json['name'], desc=request.json['desc'])
    db.session.add(app)
    db.session.commit()
    return render_template('home.html')
