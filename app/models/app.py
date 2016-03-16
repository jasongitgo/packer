from app import db

class App(db.Model):
    __tablename__ = "app"
    # __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('node_id', db.String)
    desc = db.Column('user_id', db.String)
    # data = db.Column("title", db.String)
    # content = db.Column(db.Text)
    # create_time = db.Column(db.DateTime, default=datetime.utcnow)
    # last_modify_time = db.Column(db.DateTime, default=datetime.utcnow)
    # is_publish = db.Column(db.Boolean, default=False)
    # user = relationship('User')
    # nodes = relationship('Node')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }
