from app import db

__author__ = 'jason'


class App(db.Model):
    __tablename__ = "app"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String)
    desc = db.Column('desc', db.String)
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
    name = db.Column('name', db.String)
    desc = db.Column('desc', db.String)
    appId = db.Column(db.String(20), db.ForeignKey('app.id'))

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
    name = db.Column('name', db.String)
    content = db.Column('content', db.String)
    type = db.Column('type', db.String)
    relateId = db.Column('relate_id', db.String(20))

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
    name = db.Column('name', db.String)
    isDefault = db.Column('is_default', db.Boolean)
    type = db.Column('type', db.String)
    relateId = db.Column('relate_id', db.String(20))

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
    name = db.Column('name', db.String)
    content = db.Column('content', db.String)
    templateId = db.Column('template_id', db.String(20))
    index = db.Column('index', db.INT)
    depends = db.Column('depends', db.String)

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
        return Cmd(name=d['name'], content=d['isDefault'], index=d['index'], templateId=d['templateId'],
                   depends=d['depends'])
