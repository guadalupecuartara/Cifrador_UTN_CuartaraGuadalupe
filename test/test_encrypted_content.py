import unittest
from app import create_app, db
from app.models import EncryptedContent
from cryptography.fernet import Fernet

class EncryptedContentTestCase(unittest.TestCase):
    """
    Test EncryptedContent model.
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

    def test_encrypted_content_creation(self):
        key = Fernet.generate_key()
        encrypted_content = EncryptedContent.encrypt("Hello World", key)
        self.assertEqual(encrypted_content.length, len(encrypted_content.data))
        self.assertIsNotNone(encrypted_content.key)

    def test_encrypted_content_save(self):
        key = Fernet.generate_key()
        encrypted_content = EncryptedContent.encrypt("Hello World", key)
        encrypted_content.save()
        self.assertGreaterEqual(encrypted_content.id, 1)

    def test_encrypted_content_delete(self):
        key = Fernet.generate_key()
        encrypted_content = EncryptedContent.encrypt("Hello World", key)
        encrypted_content.save()
        encrypted_content_id = encrypted_content.id
        encrypted_content.delete()
        self.assertIsNone(EncryptedContent.find(encrypted_content_id))

    def test_encrypted_content_all(self):
        key = Fernet.generate_key()
        encrypted_content = EncryptedContent.encrypt("Hello World", key)
        encrypted_content.save()
        all_contents = EncryptedContent.all()
        self.assertGreaterEqual(len(all_contents), 1)

    def test_encrypted_content_find(self):
        key = Fernet.generate_key()
        encrypted_content = EncryptedContent.encrypt("Hello World", key)
        encrypted_content.save()
        found_content = EncryptedContent.find(encrypted_content.id)
        self.assertIsNotNone(found_content)
        self.assertEqual(found_content.id, encrypted_content.id)

    def test_encrypted_content_encrypt_decrypt(self):
        key = Fernet.generate_key()
        encrypted_content = EncryptedContent.encrypt("Hello World", key)
        decrypted_content = EncryptedContent.decrypt(encrypted_content.data, key)
        self.assertEqual(decrypted_content, "Hello World")

if __name__ == '__main__':
    unittest.main()