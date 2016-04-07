#! /usr/bin/env python
# -*- coding: utf-8 -*-
import threading

import time
from app.models import db, Task, Step
import worker

process_tasks = {}


def check_task(app):
    with app.app_context():
        while True:

            tasks = db.session.query(Task).filter(Task.status == 'new').all()

            for task in tasks:
                if not process_tasks.__contains__(task.id):
                    process_tasks[task.id] = task
                    t = threading.Thread(target=process_task, args=(task, app))
                    t.start()
            time.sleep(5)


def process_task(task, app):
    with app.app_context():
        task = db.session.query(Task).filter(Task.id == task.id).one()
        task.status = 'deploying'
        db.session.commit()
        steps = Step.query.filter(Step.taskId == task.id).all()

        returncode = 0
        for step in steps:
            returncode = worker.process(step.content, step.id)
            if returncode != 0:
                step.status = 'failed'
                break
            else:
                step.status = 'success'
            step.log = worker.logs[step.id]
            worker.logs.pop(step.id)
            db.session.commit()
        if returncode != 0:
            task.status = 'failed'
        else:
            task.status = 'success'
        db.session.commit()
        del process_tasks[task.id]


def start(app):
    checker = threading.Thread(target=check_task, args=(app,))
    checker.start()