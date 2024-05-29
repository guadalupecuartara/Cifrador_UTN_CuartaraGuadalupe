from cryptography.fernet import Fernet

class EncryptedContent:
    def __init__(self, data: str, length: int, text_password: bytes):
        self.data = data  # Datos encriptados
        self.length = length  # Longitud de los datos encriptados
        self.text_password = text_password  # Clave de encriptación
    @staticmethod
    def encrypt(content: str, key: bytes) -> 'EncryptedContent':
        fernet = Fernet(key)
        encrypted = fernet.encrypt(content.encode())  # Encriptar el contenido
        return EncryptedText(encrypted.decode(), len(encrypted), key)  # Retornar EncryptedText
    @staticmethod
    def decrypt(encrypted_data: str, key: bytes) -> str:
        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted_data.encode())  # Desencriptar el contenido
        return decrypted.decode()  # Retornar el contenido desencriptado