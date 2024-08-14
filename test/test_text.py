import unittest
from flask import current_app
from app import create_app, db
from app.models import User, UserData, Text, TextHistory
from cryptography.fernet import Fernet
from app.services import UserService
from werkzeug.security import check_password_hash
from app.models import Text, TextHistory
from app.services.text_service import TextService
from app.services.encrypt_service import EncryptService

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
        self.text_service = TextService()
        self.encrypt_service = EncryptService()
        self.key = self.encrypt_service.generate_fernet_key()  # Genera una clave Fernet

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
        self.assertIsNotNone(text.histories)

    def test_text_save(self):
        text = Text(content="Hello World", language="English")
        self.text_service.save(text)
        self.assertGreaterEqual(text.id, 1)
        self.assertEqual(text.content, "Hello World")
        self.assertEqual(text.language, "English")
        self.assertEqual(text.length, len("Hello World"))
        
    def test_text_delete(self):
        text = Text(content="Hello World", language="English")
        self.text_service.save(text)
        text_id = text.id
        self.text_service.delete(text)
        self.assertIsNone(self.text_service.find(text_id))
        
    def test_text_all(self):
        text1 = Text(content="Hello World", language="English")
        text2 = Text(content="Another Text", language="Spanish")
        self.text_service.save(text1)
        self.text_service.save(text2)
        texts = self.text_service.all()
        self.assertGreaterEqual(len(texts), 2)
        
    def test_text_find(self):
        text = Text(content="Hello World", language="English")
        self.text_service.save(text)
        found_text = self.text_service.find(text.id)
        self.assertIsNotNone(found_text)
        self.assertEqual(found_text.id, text.id)
        self.assertEqual(found_text.content, text.content)
        self.assertEqual(found_text.language, text.language)
        
    def test_text_change_content(self):
    # Crear un texto y guardarlo
        text = Text(content="Initial Content", language="en")
        self.text_service.save(text)

        # Cambiar el contenido del texto
        new_content = "Updated Content"
        updated_text = self.text_service.change_content(text.id, new_content)
        
        # Verificar que el texto se actualizó correctamente
        self.assertIsNotNone(updated_text, "El texto debería ser actualizado y no ser None")
        self.assertEqual(updated_text.content, new_content, "El contenido del texto debería ser actualizado")
        
    def test_text_encrypt_decrypt_content(self):
        text = Text(content="Hello World", language="English")
        self.text_service.save(text)
        
        # Cifrar el contenido
        self.encrypt_service.encrypt_content(text, self.key)
        encrypted_content = text.encrypted_content
        self.assertNotEqual(encrypted_content, "Hello World")  # Verifica que el contenido cifrado no es igual al original
        
        # Descifrar el contenido
        self.encrypt_service.decrypt_content(text, self.key)
        self.assertEqual(text.content, "Hello World")  # Verifica que el contenido descifrado es igual al original
        
    def test_user_text(self):
        from app.models.user import User
        from app.models.user_data import UserData

        data = UserData(
            firstname = "Pablo",
            lastname = "Prats",
            address = "Address 1234",
            city = "San Rafael",
            country = "Argentina",
            phone = "54260123456789"
            )
        user = User(
            username = "pabloprats",
            password = "Qvv3r7y",
            email = "test@test.com",
            user_data=data
            )
        user_service = UserService()
        user_service.save(user)
        # Verificar que el usuario se haya guardado correctamente
        saved_user = User.query.first()
        self.assertIsNotNone(saved_user)
        self.assertEqual(saved_user.username, "pabloprats")
        self.assertEqual(saved_user.email, "test@test.com")
        # Verificar el hash de la contraseña
        self.assertTrue(check_password_hash(saved_user.password, "Qvv3r7y"))
    
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
    
    def __get_user(self):
        data = UserData()
        data.firstname = self.FIRSTNAME_PRUEBA
        data.lastname = self.LASTNAME_PRUEBA
        data.phone = self.PHONE_PRUEBA
        data.address = self.ADDRESS_PRUEBA
        data.city = self.CITY_PRUEBA
        data.country = self.COUNTRY_PRUEBA
        
        user = User(
            username=self.USERNAME_PRUEBA,
            email=self.EMAIL_PRUEBA,
            password=self.PASSWORD_PRUEBA,
            data=data  # Usa 'data' en lugar de 'user_data'
        )

        return user

if __name__ == '__main__':
    unittest.main()