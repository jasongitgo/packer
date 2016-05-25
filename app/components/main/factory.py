#! /usr/bin/env python
# -*- coding: utf-8 -*-
import threading

import time
import traceback

import celery

from app.models import db, Task, Step
import worker
from app.logger import logger

from manage import app

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


@celery.task
def test():
    with app.app_context():
        logger.info("this is celery test")
        logger.info(db.session.query(Task).filter(Task.id == '30').one().serialize())


@celery.task
def process_task(taskId):
    with app.app_context():
        try:
            task = db.session.query(Task).filter(Task.id == taskId).one()
            task.status = 'deploying'
            db.session.commit()
            steps = Step.query.filter(Step.taskId == taskId).all()

            returncode = 0
            for step in steps:
                returncode = worker.process(step.content, step.id)

                logger.info("returncode for step %s is %s" % (step.id, returncode))

                step.log = worker.logs.get(step.id, '')
                logger.info(worker.logs)
                if worker.logs.has_key(step.id):
                    worker.logs.pop(step.id)
                if returncode != 0:
                    step.status = 'failed'
                else:
                    step.status = 'success'
                db.session.commit()

                if step.status == 'failed':
                    break
            if returncode != 0:
                task.status = 'failed'
            else:
                task.status = 'success'
            db.session.commit()
            # del process_tasks[task.id]
        except Exception, e:
            logger.error('error while process task %s' % task.id)
            logger.error(traceback.format_exc())


def start(app):
    logger.info("start factory.......")
    checker = threading.Thread(target=check_task, args=(app,))
    checker.start()
