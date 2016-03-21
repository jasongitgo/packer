#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, request, jsonify

from app import App, db
from app.components.main import main


@main.route('/apps/new', methods=['GET', 'POST'])
def new_app():
    apk = App(name=request.json['name'], desc=request.json['desc'])
    db.session.add(apk)
    db.session.commit()
    return 'success'


@main.route('/apps/list', methods=['GET'])
def list_app():
    apk = App.query.all()
    print jsonify(apk)
    return jsonify({'apps': apk})
