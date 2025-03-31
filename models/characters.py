from db import db

class CharactersModel(db.Model):
    __tablename__ = "characters"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=True)
    weapon = db.Column(db.String, unique=False, nullable=True)
    
     