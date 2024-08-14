from dataclasses import dataclass
from typing import List
from app import db
from datetime import datetime
from app.models.text import Text
from sqlalchemy.dialects.postgresql import ARRAY  

@dataclass(init=False, repr=True, eq=True)
class TextHistory(db.Model):
    __tablename__ = 'text_histories'
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text_id: int = db.Column(db.Integer, db.ForeignKey('texts.id'), nullable=False)# ID del texto asociado
    content: str = db.Column(db.String(100), nullable=False)
    entries = db.Column(db.ARRAY(db.String), default=[])  # Cambiado a ARRAY de cadenas
    version = db.Column(db.Integer, nullable=False)  # Asegúrate de que esta columna esté presente
    timestamp: datetime = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    # Relación inversa con Text
    text = db.relationship('Text', back_populates='histories')

    def __init__(self, text_id, content, version, entries=None):
        self.text_id = text_id
        self.content = content
        self.version = version
        self.entries = entries or []   