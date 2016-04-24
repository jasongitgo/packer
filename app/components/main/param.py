#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request

from app import db
from app.components.main import main
from app.models import Param
from app.util import smilodon


@main.route('/param/new', methods=['GET', 'POST'])
def save_param():
    appId = request.json['appId']
    oldparams = Param.query.filter(Param.appId == appId).all()
    for old in oldparams:
        db.session.delete(old)
    db.session.commit()
    params = request.json['params']
    for param in params:
        p = Param()
        p.code = param['code']
        p.content = param['content']
        p.appId = appId
        db.session.add(p)
    db.session.commit()
    return 'success'


@main.route('/param/list', methods=['GET', 'POST'])
def list_param():
    appId = request.args['appId']
    params = Param.query.filter(Param.appId == appId).all()

    return jsonify(params=[obj.serialize() for obj in params])
