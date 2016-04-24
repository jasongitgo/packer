from app import db

__author__ = 'jason'


class App(db.Model):
    __tablename__ = "app"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String(50))
    desc = db.Column('desc', db.String(50))
    moudles = db.relationship('Moudle')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'desc': self.desc
        }

    @staticmethod
    def re_serialize(d):
        return App(name=d['name'], desc=d['desc'])


class Moudle(db.Model):
    __tablename__ = "moudle"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String(50))
    desc = db.Column('desc', db.String(50))
    appId = db.Column(db.Integer, db.ForeignKey('app.id'))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'appId': self.appId,
            'desc': self.desc
        }

    @staticmethod
    def re_serialize(d):
        return Moudle(name=d['name'], desc=d['desc'], appId=d['appId'])


class Config(db.Model):
    __tablename__ = "config"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String(50))
    content = db.Column('content', db.String(50))
    type = db.Column('type', db.String(50))
    relateId = db.Column('relate_id', db.String(50))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'relateId': self.relateId,
            'content': self.content,
            'type': self.type
        }

    @staticmethod
    def re_serialize(d):
        return Config(name=d['name'], content=d['content'], type=d['type'], relateId=d['relateId'])


class CmdTmplate(db.Model):
    __tablename__ = "cmd_template"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String(50))
    isDefault = db.Column('is_default', db.Boolean)
    type = db.Column('type', db.String(50))
    relateId = db.Column('relate_id', db.String(50))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'relateId': self.relateId,
            'isDefault': self.isDefault,
            'type': self.type
        }

    @staticmethod
    def re_serialize(d):
        return CmdTmplate(name=d['name'], isDefault=d['isDefault'], type=d['type'], relateId=d['relateId'])


class Cmd(db.Model):
    __tablename__ = "cmd"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String(50))
    content = db.Column('content', db.String(50))
    templateId = db.Column('template_id', db.String(50))
    index = db.Column('index', db.Integer)
    depends = db.Column('depends', db.String(50))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'content': self.content,
            'templateId': self.templateId,
            'index': self.index,
            'depends': self.depends
        }

    @staticmethod
    def re_serialize(d):
        return Cmd(name=d['name'], content=d['content'], index=d['index'], templateId=d['templateId'],
                   depends=d['depends'])


class Task(db.Model):
    __tablename__ = "task"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    createTime = db.Column('create_time', db.DATETIME)
    content = db.Column('content', db.String(50))
    appId = db.Column('app_id', db.String(50))
    status = db.Column('status', db.String(50))

    def serialize(self):
        return {
            'id': self.id,
            'createTime': self.createTime,
            'content': self.content,
            'appId': self.appId,
            'status': self.status
        }

    @staticmethod
    def re_serialize(d):
        return Task(createTime=d['createTime'], content=d['content'], appId=d['appId'], status=d['status'])


class Step(db.Model):
    __tablename__ = "step"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String(50))
    content = db.Column('content', db.String(50))
    log = db.Column('log', db.String(50))
    taskId = db.Column('task_id', db.String(50))
    status = db.Column('status', db.String(50))
    index = db.Column('index', db.INT)
    relateId = db.Column('relate', db.String(50))
    type = db.Column('type', db.String(50))

    def serialize(self):
        return {
            'id': self.id,
            'log': self.log,
            'content': self.content,
            'taskId': self.taskId,
            'status': self.status,
            'index': self.index,
            'relateId': self.relateId,
            'type': self.type,
            'name':self.name
        }

    @staticmethod
    def re_serialize(d):
        return Step(log=d['log'], content=d['content'], taskId=d['taskId'], status=d['status']
                    , index=d['index']
                    , relateId=d['relateId']
                    , type=d['type'])

class Param(db.Model):
    __tablename__ = "param"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String(500))
    code = db.Column('code', db.String(500))
    content = db.Column('content', db.String(500))
    type = db.Column('type', db.String(50))
    appId = db.Column('app_id', db.String(50))

    def serialize(self):
        return {
            'id': self.id,
            'code': self.code,
            'content': self.content,
            'appId': self.appId
        }

