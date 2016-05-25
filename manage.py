#!/usr/bin/env python

import os

from celery import Celery
from flask.ext.bootstrap import Bootstrap

from app import create_app, db
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager, Shell

app = create_app(os.getenv('FLASKd_CONFIG') or 'default')
bootstrap = Bootstrap(app)
manager = Manager(app)
migrate = Migrate(app, db)
ctx = app.app_context()
ctx.push()
from app.components.main import main as main_blueprint

app.register_blueprint(main_blueprint)
# from app.components.main import factory
# factory.start(app)




def make_shell_context():
    return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

def create_celery(app):
    print app.name
    c = Celery(app.name, broker='sqla+mysql://root:jason@localhost:3306/packer')
    c.conf.update(app.config)
    return c

celery = create_celery(app)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8088)
    manager.run()
