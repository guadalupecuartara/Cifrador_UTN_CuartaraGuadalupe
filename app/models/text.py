from dataclasses import dataclass
from typing import List
from app import db
from cryptography.fernet import Fernet

@dataclass(init=False, repr=True, eq=True)
class Text(db.Model):
    __tablename__ = 'texts'
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True) # ID único para cada texto
    content: str = db.Column(db.String(1200),nullable=False) # Contenido del texto
    length = db.Column(db.Integer)
    language: str = db.Column(db.String(120), nullable=False) # Lenguaje del texto
    # Relación con TextHistory
    histories = db.relationship('TextHistory', back_populates='text')
    latest_version = db.Column(db.Integer, default=0)
    user_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # Clave foránea para relacionarlo con User # ID del usuario propietario del texto
    encrypted_content: str = db.Column(db.String(1000), nullable=True)
    encrypted_content: str = db.Column(db.String(1000), nullable=True)
    encryption_key: str = db.Column(db.String(100), nullable=True)  # Almacena la clave en formato base64
    
    def __init__(self, content: str, language: str):
        self.content = content
        self.language = language
        self.length = len(content) 