#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json
from datetime import datetime

from flask import render_template, request, jsonify
from sqlalchemy import and_

from app import App, db
from app.components.main import main

from app.models import Task, Cmd, Config, Step, CmdTmplate, Moudle


@main.route('/task/new', methods=['GET', 'POST'])
def task_app():
    config = json.loads(request.json['config']['content'])
    appId = request.json['appId']
    template = request.json['template']
    moudles = request.json['moudles']

    task = Task(createTime=datetime.utcnow(), appId=appId, status='new')
    db.session.add(task)
    i = 0
    for moudle in moudles:
        if moudle.has_key('pack') and moudle['pack']:
            cmds = Cmd.query.filter(Cmd.templateId == moudle['template']['id']).all()
            # moudle_config = load_config(moudle['config']).content
            for cmd in cmds:
                # cmd = reset_cmd(cmd, moudle_config)
                c = cmd.content
                c = reset_cmd(c, config)
                step = Step(name=cmd.name, content=c, taskId=task.id, status='pending', index=i, relateId=moudle['id'],
                            type='moudle')
                i += 1
                db.session.add(step)
    cmds = Cmd.query.filter(Cmd.templateId == template['id']).all()
    for cmd in cmds:
        c = cmd.content
        c = reset_cmd(c, config)
        i += 1
        step = Step(name=cmd.name, content=c, taskId=task.id, status='pending', index=i, relateId=appId, type='app')
        db.session.add(step)
    db.session.commit()
    return jsonify(taskId=task.id)


def load_config(id):
    return Config.query.filter(Config.id == id).one()


def reset_cmd(cmd, config):
    for key, value in config.items():
        cmd = cmd.replace(r'${%s}' % key, value)
    return cmd


@main.route('/pack/loadInfos', methods=['GET'])
def load_info_for_pack():
    appId = request.args['appId']
    result = {}
    app = App.query.filter(App.id == appId).one()
    result['app'] = app.serialize()

    configs = load_configs(appId, 'app')
    result['configs'] = [c.serialize() for c in configs]

    templates = load_templates(appId, 'app')
    result['templates'] = [t.serialize() for t in templates]

    moudles = Moudle.query.filter(Moudle.appId == appId).all()
    result['moudles'] = [m.serialize() for m in moudles]
    for m in result['moudles']:
        m['configs'] = load_configs(m['id'], 'moudle')
        m['configs'] = trans_objs_json(m['configs'])

        m['templates'] = load_templates(m['id'], 'moudle')
        m['templates'] = trans_objs_json(m['templates'])
    return jsonify(infos=result)


def trans_objs_json(objs):
    return [obj.serialize() for obj in objs]


def load_configs(relate_id, t):
    configs = Config.query.filter(and_(Config.relateId == relate_id, Config.type == t)).all()
    return configs


def load_templates(relate_id, t):
    return CmdTmplate.query.filter(and_(CmdTmplate.relateId == relate_id, CmdTmplate.type == t)).all()


@main.route('/task/list', methods=['GET', 'POST'])
def list_task():
    apk = db.session.query(Task.id, Task.status, Task.createTime, App.id, App.name).filter(
        App.id == Task.appId).order_by(Task.createTime).all()
    results = []
    for a in apk:
        result = {}
        result['id'] = a[0]
        result['status'] = a[1]
        result['createTime'] = a[2]
        result['appName'] = a[4]
        results.append(result)
    return jsonify(tasks=results)


@main.route('/step/list', methods=['GET', 'POST'])
def list_step():
    steps = db.session.query(Step).filter(
        Step.taskId == request.args['taskId']).order_by(Step.index).all()

    return jsonify(steps=trans_objs_json(steps))
