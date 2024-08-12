from dataclasses import dataclass
from typing import List
from app import db
from cryptography.fernet import Fernet
from app.models.text import Text

@dataclass(init=False, repr=True, eq=True)
class EncryptedContent(db.Model):
    __tablename__ = 'encrypted'
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content : str = db.Column(db.String(1000), nullable=False)
    key: bytes = db.Column(db.LargeBinary, nullable=False)
    
    def __init__(self, data: str, length: int, text_password: bytes):
        self.data = data  # Datos encriptados
        self.length = length  # Longitud de los datos encriptados
        self.text_password = text_password  # Clave de encriptación
        
    def save(self) -> "Encriptador":
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()
    
    @classmethod
    def all(cls) -> List['Encriptador']:
        return cls.query.all()

    @classmethod
    def find(cls, id: int) -> 'Encriptador':
        return cls.query.get(id)

    @classmethod
    def find_by(cls, **kwargs) -> List['Encriptador']:
        return cls.query.filter_by(**kwargs).all()  
      
    @staticmethod
    def encrypt(content: str, key: bytes) -> 'EncryptedContent':
        fernet = Fernet(key)
        encrypted = fernet.encrypt(content.encode())  # Encriptar el contenido
        return EncryptedText(encrypted.decode(), len(encrypted), key)  # Retornar EncryptedText
    @staticmethod
    def decrypt(encrypted_data: str, key: bytes) -> str:
        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted_data.encode())  # Desencriptar el contenido
        return decrypted.decode()  # Retornar el contenido desencriptado