#! /usr/bin/env python
# -*- coding: utf-8 -*-
from flask import render_template,request

from app.components.main import main

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/app/new',methods = ['GET', 'POST'])
def app_new():
    print(1111)
    print(request.form)
    return render_template('home.html')
