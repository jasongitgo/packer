from app import db

__author__ = 'jason'


class App(db.Model):
    __tablename__ = "app"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String)
    desc = db.Column('desc', db.String)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Moudle(db.Model):
    __tablename__ = "moudle"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('name', db.String)
    desc = db.Column('desc', db.String)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }
