import logging
import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import (Cipher, algorithms, modes)


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

    def __sym_key(self) -> bytes:
        """
        Функция расшифровки симметричного ключа шифрования
        """
        try:
            with open(self.settings['secret_key'], "rb") as f:
                private_key = serialization.load_pem_private_key(
                    f.read(), password=None)
        except OSError as err:
            logging.warning(
                f"{err} ошибка чтения файла {self.settings['secret_key']}")
        try:
            with open(self.settings['symmetric_key'], "rb") as f:
                encrypted_symmetric_key = f.read()
            symmetric_key = private_key.decrypt(encrypted_symmetric_key, padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
        except OSError as err:
            logging.warning(
                f"{err} ошибка чтения файла {self.settings['symmetric_key']}")
        return symmetric_key

    def encryption(self, way: str) -> None:
        """
        Функция шифровки текста заданным алгоритмом 3DES
        """
        way_e = way
        symmetric_key = self.__sym_key()
        try:
            with open(way_e, 'r', encoding='utf-8') as f:
                text = f.read()
        except OSError as err:
            logging.warning(f"{err} ошибка чтения файла {way_e}")
        else:
            logging.info("Текст прочитан")
        padder = sym_padding.ANSIX923(128).padder()
        padded_text = padder.update(bytes(text, 'utf-8')) + padder.finalize()
        iv = os.urandom(8)
        cipher = Cipher(algorithms.TripleDES(symmetric_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        c_text = encryptor.update(padded_text) + encryptor.finalize()
        try:
            with open(self.settings['iv_path'], 'wb') as key_file:
                key_file.write(iv)
        except OSError as err:
            logging.warning(
                f"{err} ошибка записи {self.settings['iv_path']}")
        try:
            with open(self.settings['encrypted_file'], 'wb') as f_text:
                f_text.write(c_text)
        except OSError as err:
            logging.warning(
                f"{err} ошибка записи {self.settings['encrypted_file']}")
        else:
            logging.info("Тескт зашифрован")

    def decryption(self) -> str:
        """
        Функция расшифровки текста заданным алгоритмом 3DES
        """
        symmetric_key = self.__sym_key()
        try:
            with open(self.settings['encrypted_file'], 'rb') as f:
                en_text = f.read()
        except OSError as err:
            logging.warning(
                f"{err} ошибка чтения файла {self.settings['encrypted_file']}")
        try:
            with open(self.settings['iv_path'], "rb") as f:
                iv = f.read()
        except OSError as err:
            logging.warning(
                f"{err} ошибка чтения файла {self.settings['iv_path']}")
        cipher = Cipher(algorithms.TripleDES(symmetric_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        dc_text = decryptor.update(en_text) + decryptor.finalize()
        unpadder = sym_padding.ANSIX923(128).unpadder()
        unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()
        try:
            with open(self.settings['decrypted_file'], 'wb') as f:
                f.write(unpadded_dc_text)
        except OSError as err:
            logging.warning(
                f"{err} ошибка при записи в файл {self.settings['decrypted_file']}")
        else:
            logging.info("Текст расшифрован")
        return self.settings['decrypted_file']
