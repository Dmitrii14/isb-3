import os
import logging
from cryptography.hazmat.primitives import padding as symmetric_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

logger = logging.getLogger()
logger.setLevel('INFO')


class SymmetricClass:
    def __init__(self, settings: dict) -> None:
        """
        Функция инициализации
        """
        self.settings = settings

    def generation_symmetric_key(self) -> bytes:
        """
        Функция создание ключа для симметричного шифрования
        """
        symmetric_key = os.urandom(16)
        return symmetric_key

    def serealization_symmetric_key(self, key: bytes, path: str) -> None:
        """
        Функция сохранение ключа симметричного шифрования
        """
        try:
            with open(path, 'wb') as f:
                f.write(key)
        except OSError as err:
            logging.warning(f"{err} ошибка записи ключа в файл {self.settings['symmetric_key']}")

    def get_symmetric_key(self, path: str) -> bytes:
        """
        Функция загрузки ключей в файл
        """
        try:
            with open(path, 'rb') as f:
                key = f.read()
        except OSError as err:
            logging.warning(f"{err} ошибка чтения файла {self.settings['symmetric_key']}")
        return key

    def symmetric_encryption(self, key: bytes, path_message: str,
                             path_encrypted_message: str) -> None:
        """
        Функция шифровки текст с симметричным ключем
        """
        try:
            with open(path_message, 'rb') as f:
                text = f.read()
        except OSError as err:
            logging.warning(f"{err} ошибка чтения файла {path_message}")
        padder = symmetric_padding.ANSIX923(128).padder()
        padded_text = padder.update(bytes(text, 'utf-8')) + padder.finalize()
        iv = os.urandom(8)
        cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        c_text = encryptor.update(padded_text) + encryptor.finalize()
        try:
            with open(path_encrypted_message, 'wb') as f:
                f.write(c_text)
        except OSError as err:
            logging.warning(f"{err} ошибка записи {self.settings['encrypted_file']}")

    def symmetric_decryption(self, key: bytes,
                             path_encrypted_message: str,
                             path_decrypted_message: str) -> None:
        """
        Функция расшифровки текст с симметричным ключем
        """
        try:
            with open(path_encrypted_message, 'rb') as f:
                text = f.read()
        except OSError as err:
            logging.warning(f"{err} Ошибка чтения файла {self.settings['symmetric_key']}")
        try:
            with open(self.settings['iv_path'], "rb") as f:
                iv = f.read()
        except OSError as err:
            logging.warning(
                f"{err} ошибка чтения файла {self.settings['iv_path']}")
        cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        dc_text = decryptor.update(text) + decryptor.finalize()
        unpadder = symmetric_padding.ANSIX923(128).unpadder()
        unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()
        try:
            with open(path_decrypted_message, 'wb') as f:
                f.write(unpadded_dc_text)
        except OSError as err:
            logging.warning(
                f"{err} ошибка при записи в файл {self.settings['decrypted_file']}")
        else:
            logging.info("Текст расшифрован")
        return self.settings['decrypted_file']
