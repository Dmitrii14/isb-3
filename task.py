import logging
import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


logger = logging.getLogger()
logger.setLevel('INFO')


class Coding:
    def __init__(self, size: int, way: str) -> None:
        """
        Инициализация
        """
        self.size = int(size/8)
        self.way = way
        self.settings = {
            'encrypted_file': os.path.join(self.way, 'encrypted_file.txt'),
            'decrypted_file': os.path.join(self.way, 'decrypted_file.txt'),
            'symmetric_key': os.path.join(self.way, 'symmetric_key.txt'),
            'public_key': os.path.join(self.way, 'public_key.txt'),
            'secret_key': os.path.join(self.way, 'secret_key.txt'),
            'iv_path': os.path.join(self.way, 'iv_path.txt')
        }

    def generation_key(self) -> None:
        """
        Функция генерации ключей

        """
        key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        private_key = key
        public_key = key.public_key()
        try:
            with open(self.settings['public_key'], 'wb') as public_out:
                public_out.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                         format=serialization.PublicFormat.SubjectPublicKeyInfo))
        except OSError as err:
            logging.warning(
                f"{err} ошибка записи {self.settings['public_key']}")
        else:
            logging.info("Открытый ключ записан")
        try:
            with open(self.settings['secret_key'], 'wb') as private_out:
                private_out.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                            format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                            encryption_algorithm=serialization.NoEncryption()))
        except OSError as err:
            logging.warning(
                f"{err} ошибка записи {self.settings['secret_key']}")
        else:
            logging.info("Закрытый ключ записан")
        symmetric_key = os.urandom(self.size)
        encryptedtext = public_key.encrypt(symmetric_key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
                                                                       algorithm=hashes.SHA256(), label=None))
        try:
            with open(self.settings['symmetric_key'], "wb") as f:
                f.write(encryptedtext)
        except OSError as err:
            logging.warning(
                f"{err} ошибка записи {self.settings['symmetric_key']}")
        else:
            logging.info("Симметричный ключ записан")
