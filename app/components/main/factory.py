#! /usr/bin/env python
# -*- coding: utf-8 -*-
import threading

import time

from app.models import db, Task, Step
import worker

process_tasks = []


def check_task(db):
    while True:

        tasks = db.session.query(Task).filter(Task.status == 'new').all()

        for task in tasks:
            if not process_tasks.__contains__(task):
                process_tasks.append(task)
                t = threading.Thread(target=process_task, args=(task,))
                t.start()
        time.sleep(5)


def process_task(task):
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
        step.log = worker.log[step.id]
        worker.log.pop(step.id)
        db.session.commit()
    if returncode != 0:
        task.status = 'failed'
    else:
        task.status = 'success'
    db.session.commit()


def start():
    checker = threading.Thread(target=check_task, args=(db,))
    checker.start()
