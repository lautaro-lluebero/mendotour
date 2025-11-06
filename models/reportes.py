from models.db import db
from datetime import datetime

class Reportes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    tipo = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship(
        'Users',
        backref=db.backref('reportes', lazy=True, cascade="all, delete-orphan")
    )

    def __init__(self, user_id, tipo):
        self.user_id = user_id
        self.tipo = tipo

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'tipo': self.tipo,
            'fecha': self.fecha.strftime("%Y-%m-%d %H:%M:%S")
        }
