from dataclasses import dataclass
from typing import List
from app import db

@dataclass(init=False, repr=True, eq=True)
class TextHistory(db.Model):
    __tablename__ = 'text_histories'
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content: str = db.Column(db.String, nullable=False)
    entries: List[str] = db.Column(db.PickleType, default=[])
#continuar