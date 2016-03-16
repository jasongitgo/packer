#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template

from app.components.main import main

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/app/new')
def home():
    print
    return render_template('home.html')
