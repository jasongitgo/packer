#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify, request

from app import db
from app.components.main import main
from app.models import Param


@main.route('/param/new', methods=['GET', 'POST'])
def save_param():
    appId = request.json['appId']
    params = request.json['params']
    for param in params:
        p = Param()
        p.code = param['code']
        p.content = params['content']
        p.appId = appId
        db.session.add(p)
    db.session.commit()
    return 'success'

