from db import db
from sqlalchemy import UniqueConstraint

class Party(db.Model):
    __tablename__ = "party"

    id = db.Column(db.Integer, primary_key=True) 
    save_id = db.Column(
        db.String,
        db.ForeignKey(
            "saves.id",
            ondelete="CASCADE",
            name="fk_party_save_id",
        ),
        nullable=False,
        unique=True,
    )

    __table_args__ = (
        db.UniqueConstraint(
            "save_id",
            name="uq_party_save_id",
        ),
    )