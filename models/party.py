from db import db

class PartyModel(db.Model):
    __tablename__ = "party"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False) 
    # materia = db.relationship("MateriaModel", back_populates="party", lazy="dynamic")
    
     