from dataclasses import dataclass
from typing import List,Optional
from app import db
from app.models.text import Text
from sqlalchemy.dialects.postgresql import ARRAY  

@dataclass(init=False, repr=True, eq=True)
class TextHistory(db.Model):
    __tablename__ = 'text_histories'
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text_id: int = db.Column(db.Integer, db.ForeignKey('texts.id'), nullable=False)# ID del texto asociado
    content: str = db.Column(db.String(100), nullable=False)
    entries = db.Column(db.ARRAY(db.String), default=[])  # Cambiado a ARRAY de cadenas
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    # Relación inversa con Text
    text = db.relationship('Text', back_populates='histories')
    
    def add_entry(self, entry: str) -> None:
        if self.entries is None:
            self.entries = []  # Inicializa si es None
        self.entries.append(entry)
        db.session.commit()
   
    def view_history(self) -> list:
        return self.entries if self.entries is not None else []
   
    def save(self) -> "TextHistory":
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find(cls, id: int) -> "TextHistory":
        return cls.query.get(id)
    
    @classmethod
    def find_by(cls, **kwargs) -> List["TextHistory"]:
        return cls.query.filter_by(**kwargs).all()

    @staticmethod
    def view_versions(text_id: int) -> List["TextHistory"]:
        return (
        TextHistory.query.filter_by(text_id=text_id)
        .order_by(TextHistory.timestamp.desc())
        .all() )
        
    def change_version(self, version_id: int) -> Optional[str]:
        version = TextHistory.query.filter_by(id=version_id, text_id=self.text_id).first()# Buscar la versión específica del texto por su ID
        if version:
            self.content = version.content# Actualizar el contenido del texto a la versión seleccionada
            db.session.commit()
            return self.content
        else:
            return None  # La versión no fue encontrada
