from dataclasses import dataclass
from typing import List
from app import db
#from .encrypted_content import EncryptedContent
#from .text_history import TextHistory

@dataclass(init=False, repr=True, eq=True)
class Text(db.Model):
    __tablename__ = 'texts'
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True) # ID único para cada texto
    content: str = db.Column(db.String(120),nullable=False) # Contenido del texto
    length: int = db.Column(db.Integer, nullable=False) # Longitud del texto
    language: str = db.Column(db.String(120), nullable=False) # Lenguaje del texto
    history = db.relationship('TextHistory', backref='text', uselist=False) # Relación uno a uno con TextHistory
    user_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # ID del usuario propietario del texto
    encryptor_id: int = db.Column(db.Integer, db.ForeignKey('encryptors.id'), nullable=True) 
    encryptor= db.relationship('Encryptor', backref="text",uselist=False)
    
    def __init__(self, content: str, language: str):
        self.content = content
        self.language = language
        self.length = len(content) #Calcular la longitud del texto 
        from app.models.text_history import TextHistory
        self.history = TextHistory(content=content) # Crear un nuevo historial de texto
    
    def change_content(self, new_content: str) -> None:
        self.content = new_content
        self.length = len(new_content)
        db.session.commit()
        
    def save(self) -> 'Text':
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def all(cls) -> List['Text']:
        return cls.query.all()

    @classmethod
    def find(cls, id: int) -> 'Text':
        return cls.query.get(id)

    @classmethod
    def find_by(cls, **kwargs) -> List['Text']:
        return cls.query.filter_by(**kwargs).all()

    def encrypt_content(self, key: bytes) -> 'EncryptedContent':
        from .encrypted_content import EncryptedContent
        return EncryptedContent.encrypt(self.content, key)

    def decrypt_content(self, key: bytes) -> str:
        from .encrypted_content import EncryptedContent
        return EncryptedContent.decrypt(self.content, key)