from db import db

class EnemyModel(db.Model):
    __tablename__ = "enemies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    hp = db.Column(db.Integer, unique=False, nullable=False)
    description = db.Column(db.String, unique=False, nullable=True)
    steal = db.Column(db.String, unique=False, nullable=True)
    location = db.Column(db.String, unique=False, nullable=False)
    disc = db.Column(db.String, unique=False, nullable=False)


     