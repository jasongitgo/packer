#!/usr/bin/env python

import os
import time

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
from app.components.main import factory
factory.start(app)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    try:
        pid = os.fork()

        if pid == 0:
            # logger.info( "this is child process.")
            time.sleep(3)
            app.run(host='0.0.0.0', port=8088)
        else:
            # logger.info( "this is parent process.")
            pass

    except OSError, e:
        pass

    #manager.run()
