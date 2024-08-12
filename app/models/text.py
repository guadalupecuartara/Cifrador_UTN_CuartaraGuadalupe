from dataclasses import dataclass
from typing import List
from app import db
from app.models.encrypted_content import EncryptedContent

@dataclass(init=False, repr=True, eq=True)
class Text(db.Model):
    __tablename__ = 'texts'
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True) # ID único para cada texto
    content: str = db.Column(db.String(120),nullable=False) # Contenido del texto
    length: int = db.Column(db.Integer, nullable=False) # Longitud del texto
    language: str = db.Column(db.String(120), nullable=False) # Lenguaje del texto
    history = db.relationship('TextHistory', backref='text', lazy=True) # Relación uno a uno con TextHistory
    user_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # ID del usuario propietario del texto
    encryptor_id: int = db.Column(db.Integer, db.ForeignKey('encrypted.id'), nullable=True) 
    encryptor= db.relationship('EncryptedContent', backref="text",uselist=False)
    
    def __init__(self, content: str, language: str):
        self.content = content
        self.language = language
        self.length = len(content) #Calcular la longitud del texto 
        from app.models.text_history import TextHistory
        self.history = TextHistory(content=content) # Crear un nuevo historial de texto
    
    def change_content(self, new_content: str) -> None:
         # Cambia el contenido del texto y guarda la versión anterior en TextHistory.
        from app.models.text_history import TextHistory  # Importa dentro de la función o método

        old_content = self.content
        self.content = new_content
        history = TextHistory(text_id=self.id, content=old_content)
        history.save()
        
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