from app import db
from datetime import datetime
from sqlalchemy.orm import relationship


class Note(db.Model):
    __tablename__ = "notes"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    node_id = db.Column('node_id', db.Integer, db.ForeignKey('nodes.id'))
    user_id = db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
    data = db.Column("title", db.String)
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    last_modify_time = db.Column(db.DateTime, default=datetime.utcnow)
    is_publish = db.Column(db.Boolean, default=False)
    user = relationship('User')
    nodes = relationship('Node')

    def serialize(self):
        return {
            'id': self.id,
            'node': {
                'id': self.nodes.id,
                'name': self.nodes.text
            },
            'content': self.content
        }
