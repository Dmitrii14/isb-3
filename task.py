import logging
import os

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
