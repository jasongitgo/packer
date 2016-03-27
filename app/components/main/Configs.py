#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import jsonify

from app.components.main import main


@main.route('/configs/template', methods=['GET', 'POST'])
def load_config_template():
    f = open('app/components/template/config.template', 'rb')
    config = f.read()
    f.close()
    return jsonify(config=config)
