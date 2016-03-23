#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template, request, jsonify

from app import db, config
from app.components.main import main
from app.models import Config


@main.route('/configs/new', methods=['GET', 'POST'])
def new_config():
    id = request.json['id']
    if id:
        config = Config.query.filter(Config.id == id).one()
        config.name = request.json['name']
        config.content = request.json['content']
        db.session.commit()
    else:
        config = Config(name=request.json['name'], content=request.json['content'])
        db.session.add(config)
        db.session.commit()
    return 'success'


@main.route('/configs/list', methods=['GET'])
def list_config():
    configs = Config.query.filter(Config.id == request.args['id'])
    return jsonify(configs=[config.serialize() for config in configs])


@main.route('/configs/select', methods=['GET', 'POST'])
def select_config():
    config = Config.query.filter(Config.id == request.args['id']).first()
    return jsonify(config=config.serialize())
