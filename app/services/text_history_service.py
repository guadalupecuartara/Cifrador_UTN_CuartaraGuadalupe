from typing import List
from app import db
from app.models.text_history import TextHistory,Text
from app.repositories.text_history_repository import TextHistoryRepository
from app.repositories.text_repository import TextRepository

class TextHistoryService:
    def __init__(self):
        self.text_history_repository = TextHistoryRepository()
        self.text_repository = TextRepository()


    def save(self, text_history: TextHistory) -> TextHistory:
        """ Guarda un objeto TextHistory en la base de datos. """
        return self.text_history_repository.save(text_history)

    def find_by_text_id(self, text_id: int) -> List[TextHistory]:
        """ Encuentra todas las versiones del texto asociadas a un text_id específico. """
        return self.text_history_repository.find_by_text_id(text_id)

    def find_version(self, text_id: int, version: int) -> TextHistory:
        """ Encuentra una versión específica de un texto por text_id y version_number. """
        return self.text_history_repository.find_version(text_id, version)

    def delete(self, text_history: TextHistory) -> None:
        """ Elimina un objeto TextHistory de la base de datos. """
        self.text_history_repository.delete(text_history)

    def revert_to_version(self, text_id: int, version: int) -> Text:
        """ Revertir el contenido del texto a una versión específica. """
        text_history = self.find_version(text_id, version)
        if text_history:
            text = self.text_repository.find(text_id)
            if text:
                text.content = text_history.content
                self.text_repository.save(text)
                return text
        return None
    def get_versions(self, text_id: int) -> List[int]:
        """ Obtiene una lista de todos los números de versión para un text_id específico. """
        histories = self.find_by_text_id(text_id)
        return [history.version for history in histories]
    
    def create_text_history(self, text_id: int, content: str, version: int) -> TextHistory:
        """ Crea y guarda una nueva entrada en el historial de texto. """
        text_history = TextHistory(
            text_id=text_id,
            content=content,
            version=version
        )
        return self.save(text_history)