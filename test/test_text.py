import unittest
from flask import current_app
from app import create_app, db
from app.models import User, UserData, Text, TextHistory
from cryptography.fernet import Fernet
from app.services import UserService

class TextTestCase(unittest.TestCase):
    """
    Test Text model
    Aplica principios como DRY (Don't Repeat Yourself), KISS (Keep It Simple, Stupid),
    YAGNI (You Aren't Gonna Need It), y SOLID (Single Responsibility Principle).
    """
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app(self):
        self.assertIsNotNone(current_app)

    def test_text_creation(self):
        text = Text(content="Hello World", language="English")
        self.assertEqual(text.content, "Hello World")
        self.assertEqual(text.language, "English")
        self.assertEqual(text.length, len("Hello World"))
        self.assertIsNotNone(text.history)

    def test_text_save(self):
        text = Text(content="Hello World", language="English")
        text.save()
        self.assertGreaterEqual(text.id, 1)
        self.assertEqual(text.content, "Hello World")
        self.assertEqual(text.language, "English")
        self.assertEqual(text.length, len("Hello World"))

    def test_text_delete(self):
        text = Text(content="Hello World", language="English")
        text.save()
        text_id = text.id
        text.delete()
        self.assertIsNone(Text.find(text_id))

    def test_text_all(self):
        text = Text(content="Hello World", language="English")
        text.save()
        texts = Text.all()
        self.assertGreaterEqual(len(texts), 1)

    def test_text_find(self):
        text = Text(content="Hello World", language="English")
        text.save()
        found_text = Text.find(text.id)
        self.assertIsNotNone(found_text)
        self.assertEqual(found_text.id, text.id)
        self.assertEqual(found_text.content, text.content)
        self.assertEqual(found_text.language, text.language)

    def test_text_change_content(self):
        text = Text(content="Hello World", language="English")
        text.save()
        old_content = text.content
        new_content = "New Content"
        text.change_content(new_content)
        self.assertEqual(text.content, "New Content")
        self.assertEqual(text.length, len("New Content"))
        
        # Verifica que se haya guardado la versión anterior en TextHistory
        history = TextHistory.query.filter_by(text_id=text.id).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.content, old_content)

    def test_text_encrypt_decrypt_content(self):
        text = Text(content="Hello World", language="English")
        text.save()
        encrypted_content = text.encrypted_content
        decrypted_content = text.decrypt_content()
        self.assertEqual(decrypted_content, "Hello World")

    def test_user_text(self):
        from app.models.user import User
        from app.models.user_data import UserData

        data = UserData()
        data.firstname = "Pablo"
        data.lastname = "Prats"
        data.address = "Address 1234"
        data.city = "San Rafael"
        data.country = "Argentina"
        data.phone = "54260123456789"

        user = User(data)
        user.email = "test@test.com"
        user.username = "pabloprats"
        user.password = "Qvv3r7y"
        user_service = UserService()
        user_service.save(user)

if __name__ == '__main__':
    unittest.main()