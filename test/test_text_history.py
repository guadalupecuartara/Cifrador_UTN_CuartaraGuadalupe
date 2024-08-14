import unittest
from flask import current_app
from app import create_app, db
from app.models.text import Text
from app.models.text_history import TextHistory
from app.services.text_history_service import TextHistoryService
from app.services.text_service import TextService
from app.repositories.text_history_repository import TextHistoryRepository
from app.repositories.text_repository import TextRepository

class TextHistoryTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.text_history_service = TextHistoryService()
        self.text_service = TextService()
        self.text_repository = TextRepository()
        self.text_history_repository = TextHistoryRepository()

        # Create a text object to use in tests
        self.text = Text(content='Sample Content', language='English')
        self.text_service.save(self.text)
        db.session.commit()  # Ensure the text is committed to the database

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app(self):
        self.assertIsNotNone(current_app)

    def test_text_history_creation(self):
        text_history = TextHistory(
            text_id=self.text.id,
            content='Initial Version',
            version=1
        )
        db.session.add(text_history)
        db.session.commit()
        
        # Verifica que el texto histórico se haya creado correctamente
        self.assertIsNotNone(text_history.id)
        self.assertEqual(text_history.content, 'Initial Version')
        self.assertEqual(text_history.version, 1)
        self.assertIsNotNone(text_history.timestamp)
        
    def test_text_history_save(self):
        text = Text(content="Sample Text", language="English")
        self.text_service.save(text)
        
        text_history = TextHistory(text_id=text.id, content="Version 1", version=1)
        self.text_history_service.save(text_history)
        
        self.assertGreaterEqual(text_history.id, 1)
        self.assertEqual(text_history.content, "Version 1")

    def test_text_history_delete(self):
        text = Text(content="Sample Text", language="English")
        self.text_service.save(text)
        
        text_history = TextHistory(text_id=text.id, content="Version 1", version=1)
        self.text_history_service.save(text_history)
        text_history_id = text_history.id
        self.text_history_service.delete(text_history)
        
        deleted_history = self.text_history_repository.find_version(text.id, text_history.version)
        self.assertIsNone(deleted_history)

    def test_text_history_all(self):
        text1 = Text(content="Text 1", language="English")
        text2 = Text(content="Text 2", language="Spanish")
        self.text_service.save(text1)
        self.text_service.save(text2)
        
        text_history1 = TextHistory(text_id=text1.id, content="Version 1", version=1)
        text_history2 = TextHistory(text_id=text2.id, content="Version 2", version=1)
        self.text_history_service.save(text_history1)
        self.text_history_service.save(text_history2)
        
        histories = self.text_history_repository.all()
        self.assertGreaterEqual(len(histories), 2)

    def test_text_history_find_version(self):
        self.text_history_service.save(TextHistory(
            text_id=self.text.id,
            content='Version 1',
            version=1
        ))
        
        text_history = self.text_history_service.find_version(self.text.id, 1)
        self.assertIsNotNone(text_history)
        self.assertEqual(text_history.content, 'Version 1')

    def test_text_history_find_by_text_id(self):
        text = Text(content="Sample Text", language="English")
        self.text_service.save(text)
        
        text_history1 = TextHistory(text_id=text.id, content="Version 1", version=1)
        text_history2 = TextHistory(text_id=text.id, content="Version 2", version=2)
        self.text_history_service.save(text_history1)
        self.text_history_service.save(text_history2)
        
        histories = self.text_history_service.find_by_text_id(text.id)
        self.assertEqual(len(histories), 2)

    def test_text_history_revert_to_version(self):
        self.text_history_service.save(TextHistory(
            text_id=self.text.id,
            content='Version 1',
            version=1
        ))
        self.text_history_service.save(TextHistory(
            text_id=self.text.id,
            content='Version 2',
            version=2
        ))
        
        self.text_history_service.revert_to_version(self.text.id, 1)
        text = self.text_repository.find(self.text.id)
        self.assertEqual(text.content, 'Version 1')

    def test_text_history_get_versions(self):
        self.text_history_service.save(TextHistory(
            text_id=self.text.id,
            content='Version 1',
            version=1
        ))
        self.text_history_service.save(TextHistory(
            text_id=self.text.id,
            content='Version 2',
            version=2
        ))
        
        versions = self.text_history_service.get_versions(self.text.id)
        self.assertEqual(versions, [1, 2])
        
if __name__ == '__main__':
    unittest.main()