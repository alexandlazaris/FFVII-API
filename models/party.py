from db import db
import uuid

class Party(db.Model):
    __tablename__ = "party"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
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