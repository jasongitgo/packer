#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, request, jsonify

from app import db, Moudle
from app.components.main import main


@main.route('/moudles/new', methods=['GET', 'POST'])
def new_moudle():
    moudle = Moudle(appId=request.json['appId'], name=request.json['name'], desc=request.json['desc'])
    db.session.add(moudle)
    db.session.commit()
    return 'success'


@main.route('/moudles/list', methods=['GET'])
def list_moudle():
    moudles = Moudle.query.filter(Moudle.appId == request.args['appId'])
    return jsonify(moudles=[moudle.serialize() for moudle in moudles])


@main.route('/moudles/select', methods=['GET', 'POST'])
def select_moudle():
    apk = Moudle.query.filter(Moudle.id == request.args['id']).first()
    return jsonify(moudle=apk.serialize())
