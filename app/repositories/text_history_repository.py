from typing import List
from app.models.text_history import TextHistory
from app import db

class TextHistoryRepository:
    def save(self, text_history: TextHistory) -> TextHistory:
        db.session.add(text_history)
        db.session.commit()
        return text_history

    def delete(self, text_history: TextHistory) -> None:
        db.session.delete(text_history)
        db.session.commit()
        
    def all(self) -> List[TextHistory]:
        return db.session.query(TextHistory).all()

    def find_version(self, text_id: int, version_number: int) -> TextHistory:
        """ Encuentra una versión específica de un texto por text_id y version_number. """
        return db.session.query(TextHistory).filter_by(text_id=text_id, version=version_number).first()

    def find_by_text_id(self, text_id: int) -> List[TextHistory]:
        """ Encuentra todas las versiones del texto asociadas a un text_id específico. """
        return db.session.query(TextHistory).filter_by(text_id=text_id).all()

    def revert_to_version(self, text_id: int, version_number: int) -> TextHistory:
        """ Revertir el contenido del texto a una versión específica. """
        text_history = self.find_version(text_id, version_number)
        if text_history:
            text = db.session.query(TextHistory).filter_by(id=text_id).first()
            if text:
                text.content = text_history.content
                db.session.commit()
                return text
        return None

    def get_versions(self, text_id: int) -> List[int]:
        """ Obtiene una lista de todos los números de versión para un text_id específico. """
        histories = self.find_by_text_id(text_id)
        return [history.version for history in histories]
    
    def find_latest_version(self, text_id: int) -> TextHistory:
        """
        Encuentra la última versión del historial para un texto dado.
        
        :param text_id: ID del texto cuyo historial se está buscando
        :return: Instancia de TextHistory con la versión más alta o None si no se encuentra
        """
        return db.session.query(TextHistory).filter_by(text_id=text_id).order_by(TextHistory.version_number.desc()).first()
    