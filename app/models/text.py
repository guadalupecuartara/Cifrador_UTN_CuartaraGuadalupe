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
    histories = db.relationship('TextHistory', backref='related_text', lazy=True, cascade='all, delete-orphan')
    user_id: int = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True) # Clave foránea para relacionarlo con User # ID del usuario propietario del texto
    encrypted_content: str = db.Column(db.String(1000), nullable=True)
    encryption_key: bytes = db.Column(db.LargeBinary, nullable=True)

    def __init__(self, content: str, language: str):
        self.content = content
        self.language = language
        self.length = len(content) #Calcular la longitud del texto 
        self.encryption_key = Fernet.generate_key()  # Generar una clave de encriptación
        self.encrypt_content()
    
    def encrypt_content(self) -> None:
        fernet = Fernet(self.encryption_key)
        self.encrypted_content = fernet.encrypt(self.content.encode()).decode()
    
    def decrypt_content(self) -> str:
        fernet = Fernet(self.encryption_key)
        return fernet.decrypt(self.encrypted_content.encode()).decode()
    
    def change_content(self, new_content: str) -> None:
         # Cambia el contenido del texto y guarda la versión anterior en TextHistory.
        from app.models.text_history import TextHistory  # Importa dentro de la función o método

        old_content = self.content
        self.content = new_content
        self.encrypt_content()  # Encriptar el nuevo contenido
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