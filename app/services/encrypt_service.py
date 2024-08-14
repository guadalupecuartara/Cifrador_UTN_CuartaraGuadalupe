from cryptography.fernet import Fernet
from app.models import Text
from app.repositories.text_repository import TextRepository  # Asegúrate de que la ruta de importación sea correcta
import base64

text_repository = TextRepository()

class EncryptService:
    def __init__(self):
        self.text_repository = TextRepository()

    def generate_fernet_key(self) -> bytes:
        """
        Genera una clave Fernet.
        :return: Clave Fernet en formato bytes
        """
        return Fernet.generate_key()

    def encrypt_content(self, text: Text, key: bytes, auto_save: bool = True) -> None:
        """
        Cifra el contenido de un objeto Text utilizando una clave Fernet.
        :param text: Objeto Text a cifrar
        :param key: Clave Fernet en formato bytes
        :param auto_save: Si es True, guarda automáticamente el objeto Text cifrado en la base de datos
        """
        fernet = Fernet(key)
        encrypted_content = fernet.encrypt(text.content.encode('utf-8'))
        text.encrypted_content = base64.b64encode(encrypted_content).decode('utf-8')
        text.encryption_key = base64.b64encode(key).decode('utf-8')

        if auto_save:
            self.text_repository.save(text)

    def decrypt_content(self, text: Text, key: bytes, auto_save: bool = True) -> None:
        """
        Descifra el contenido de un objeto Text utilizando una clave Fernet.
        :param text: Objeto Text a descifrar
        :param key: Clave Fernet en formato bytes
        :param auto_save: Si es True, guarda automáticamente el objeto Text descifrado en la base de datos
        """
        fernet = Fernet(key)
        encrypted_content = base64.b64decode(text.encrypted_content)
        decrypted_content = fernet.decrypt(encrypted_content)
        text.content = decrypted_content.decode('utf-8')

        if auto_save:
            self.text_repository.save(text)

    def generate_key_from_string(self, key_string: str) -> bytes:
        """
        Convierte una clave en formato string a bytes, usando base64.
        :param key_string: Clave en formato string
        :return: Clave en formato bytes
        """
        return base64.b64decode(key_string)