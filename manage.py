#!/usr/bin/env python

import os

from flask.ext.bootstrap import Bootstrap

from app import create_app, db
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.script import Manager, Shell

app = create_app(os.getenv('FLASKd_CONFIG') or 'default')
bootstrap = Bootstrap(app)
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8088)
    manager.run()
