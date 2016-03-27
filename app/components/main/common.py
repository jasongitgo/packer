#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, request, jsonify
from sqlalchemy import and_

from app.models import App, db, Moudle, CmdTmplate, Cmd, Config
from app.components.main import main

map = {'app': App, 'moudle': Moudle, 'config': Config, 'cmd': Cmd, 'cmdtemplate': CmdTmplate}


@main.route('/common/new', methods=['POST'])
def new_entity():
    key = request.json['_type']

    if request.json['entity'].has_key('id'):
        id = request.json['entity']['id']
        obj = map[key].query.filter(map[key].id == id).one()
        for k, v in request.json['entity'].items():
            for k1, v1 in map[key].__dict__.items():
                if k1 == k:
                    obj.__setattr__(k, v)
        db.session.commit()
    else:
        entity = map[key].re_serialize(request.json['entity'])
        db.session.add(entity)
        db.session.commit()
    return 'success'


@main.route('/common/list', methods=['GET'])
def list_entities():
    args = request.args
    key = args['_type']
    query = map[key].query
    condions = []
    for k, v in args.items():
        if k != '_type':
            condions.append(map[key].__dict__[k] == v)
    entities = query.filter(and_(*condions)).all()
    return jsonify(entities=[entity.serialize() for entity in entities])


@main.route('/common/select', methods=['GET'])
def select_entity():
    key = request.args['_type']

    apk = map[key].query.filter(map[key].id == request.args['id']).first()
    return jsonify(entity=apk.serialize())


@main.route('/common/delete', methods=['GET'])
def delete_entity():
    key = request.args['_type']

    map[key].query.filter(map[key].id == request.args['id']).delete()
    return 'success'
