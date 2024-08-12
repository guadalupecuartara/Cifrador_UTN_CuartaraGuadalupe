from dataclasses import dataclass
from typing import List,Optional
from app import db
from app.models.text import Text

@dataclass(init=False, repr=True, eq=True)
class TextHistory(db.Model):
    __tablename__ = 'text_histories'
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content: str = db.Column(db.String(100), nullable=False)
    entries: List[str] = db.Column(db.PickleType, default=[]) 
    text_id: int = db.Column(db.Integer, db.ForeignKey('texts.id'), nullable=False)# ID del texto asociado
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def add_entry(self, entry: str) -> None:
        self.entries.append(entry)  
        db.session.commit()

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
    
    def view_history(self) -> List[str]:
        return self.entries

    @staticmethod
    def view_versions(self) -> List[int]:
        versions = TextHistory.query.filter_by(text_id=self.text_id).order_by(TextHistory.id.asc()).all()  # Obtener todas las versiones anteriores del texto
        return [version.id for version in versions] # Retornar una lista de los IDs de las versiones

    def change_version(self, version_index: int) -> Optional[str]:
        version = TextHistory.query.filter_by(id=version_id, text_id=self.text_id).first()# Buscar la versión específica del texto por su ID
        if version:
            self.content = version.content# Actualizar el contenido del texto a la versión seleccionada
            db.session.commit()
            return self.content
        else:
            return None  # La versión no fue encontrada
