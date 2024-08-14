from typing import List
from app.models import Text ,TextHistory
from app import db

class TextRepository:
    
    def save(self, text: Text) -> Text:
        db.session.add(text)
        db.session.commit()
        return text

    def update(self, text: Text, id: int) -> Text:
        existing_text = db.session.query(Text).filter_by(id=id).first()
        if existing_text:
            existing_text.content = text.content
            existing_text.language = text.language
            db.session.commit()
        return existing_text
    
    def delete(self, text: Text) -> None:
        db.session.delete(text)
        db.session.commit()

    def all(self) -> List[Text]:
        return db.session.query(Text).all()

    def find(self, id: int) -> Text:
        return db.session.query(Text).filter_by(id=id).first()
    
    def find_by(self, **kwargs) -> List[Text]:
        return db.session.query(Text).filter_by(**kwargs).all()
   