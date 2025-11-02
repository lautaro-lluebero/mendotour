from models.db import db

class Opinion(db.Model):
    __tablename__ = 'opiniones'
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, nullable=False)
    contenido  = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
