from typing import List
from app import db 
from app.models import Text, TextHistory
from app.repositories import TextRepository, TextHistoryRepository
from app.services.security import SecurityManager, WerkzeugSecurity  # Asegúrate de que la ruta de importación sea correcta

class TextService:
    def __init__(self) -> None:
        self.__security = SecurityManager(WerkzeugSecurity())
        self.text_repository = TextRepository()  # Inicializa aquí las instancias
        self.text_history_repository = TextHistoryRepository()

    def save(self, text: Text) -> Text:
        return self.text_repository.save(text)

    def update(self, text: Text, id: int) -> Text:
        return self.text_repository.update(text, id)

    def delete(self, text: Text) -> None:
        self.text_repository.delete(text)

    def all(self) -> List[Text]:
        return self.text_repository.all()

    def find(self, id: int) -> Text:
        return self.text_repository.find(id)

    def find_by(self, **kwargs) -> List[Text]:
        return self.text_repository.find_by(**kwargs)
    
    def change_content(self, text_id: int, new_content: str) -> Text:
        text = self.find(text_id)
        if text:
            # Guardar el historial actual
            latest_version = self.text_history_repository.find_version(text_id, text.latest_version)
            if latest_version:
                new_version = latest_version.version + 1
            else:
                new_version = 1

            text_history = TextHistory(
                text_id=text_id,
                content=text.content,
                version=new_version
            )
            self.text_history_repository.save(text_history)

            # Actualizar el contenido del texto
            text.content = new_content
            text.length = len(new_content)
            db.session.commit()

            return text
        return None