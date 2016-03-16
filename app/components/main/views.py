#! /usr/bin/env python
# -*- coding: utf-8 -*-
from app.components.main import main
from config import basedir
from flask import render_template, send_from_directory, request


@main.route('/')
def home():
    return render_template('home.html')
