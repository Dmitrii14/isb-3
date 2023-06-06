import logging
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import \
    padding as asymmetric_padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import (load_pem_private_key,
                                                          load_pem_public_key)

logger = logging.getLogger()
logger.setLevel('INFO')


class AsymmetricClass:
    def __init__(self, settings: dict) -> None:
        """
        Функция инициализации
        """
        self.settings = settings

    def generation_asymmetric_keys(self) -> tuple:
        """
        Функция создание ключа для асимметричного шифрования
        """
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        private_key = key
        public_key = key.public_key()
        return private_key, public_key

    def serialization_asymmetric_keys(self, public_key: rsa.RSAPublicKey,
                                      private_key: rsa.RSAPrivateKey,
                                      public_pem: str,
                                      private_pem: str) -> None:
        """
        Функция сохранение ключа асимметричного шифрования
        """
        private_key_serialized = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_key_serialized = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        try:
            with open(public_pem, 'wb') as f:
                f.write(public_key_serialized)
        except OSError as err:
            logging.warning(f"{err} ошибка записи {self.settings['public_key']}")
        try:
            with open(private_pem, 'wb') as f:
                f.write(private_key_serialized)
        except OSError as err:
            logging.warning(f"{err} ошибка записи {self.settings['secret_key']}")

    def get_public_key(self, public_pem: str) -> rsa.RSAPublicKey:
        """
        Функция загрузки открытого ключа в файл
        """
        try:
            with open(public_pem, 'rb') as f:
                public_key_deserialized = f.read()
            public_key = load_pem_public_key(
                public_key_deserialized)
        except OSError as err:
            logging.warning(f"{err} ошибка записи {self.settings['public_key']}")
        return public_key

    def get_private_key(self, private_pem: str) -> rsa.RSAPrivateKey:
        """
        Функция загрузки закрытого ключа в файл
        """
        try:
            with open(private_pem, 'rb') as f:
                private_key_deserialized = f.read()
            private_key = load_pem_private_key(
                private_key_deserialized, password=None)
        except OSError as err:
            logging.warning(f"{err} ошибка записи {self.settings['secret_key']}")
        return private_key

    def encryption_symmetric_key(self,
                                 public_key: rsa.RSAPublicKey,
                                 symmetric_key: bytes) -> bytes:
        """
        Функция позваляет шифровать симметричный ключ с помощью асимметричного шифрования
        """
        encrypted_symmetric_key = public_key.encrypt(
            symmetric_key,
            asymmetric_padding.OAEP(
                mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted_symmetric_key

    def decryption_symmetric_key(self,
                                 private_key: rsa.RSAPrivateKey,
                                 encrypted_symmetric_key: bytes) -> bytes:
        """
        Функция позваляет расшифровывать симметричный ключ с помощью асимметричного шифрования
        """
        symmetric_key = private_key.decrypt(
            encrypted_symmetric_key,
            asymmetric_padding.OAEP(
                mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return symmetric_key
