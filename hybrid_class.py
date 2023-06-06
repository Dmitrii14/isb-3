import json
import logging
import asymmetric_class
import symmetric_class

logger = logging.getLogger()
logger.setLevel('INFO')


class HybridClass:
    def __init__(self, path_json: str) -> None:
        """
        Функция инициализации
        """
        try:
            with open(path_json) as f:
                self.settings = json.load(f)
        except OSError as err:
            logging.warning(
                f"{err} Настройки по умолчанию не загружаются")
        try:
            self.symmetric_sys = symmetric_class.SymmetricClass(self.settings)
            self.asymmetric_sys = asymmetric_class.AsymmetricClass(self.settings)
        except Exception as err:
            raise

    def generation_keys(self) -> None:
        """
        Функция генерирует симметричный ключ, асимметричные ключи и сериализует их
        """
        symmetric_key = self.symmetric_sys.generation_symmetric_key()
        private_key, public_key = self.asymmetric_sys.generation_asymmetric_keys()
        encrypted_symmetric_key = self.asymmetric_sys.encryption_symmetric_key(
            public_key, symmetric_key)
        self.asymmetric_sys.serialization_asymmetric_keys(
            public_key, private_key,
            self.settings['public_key'], self.settings['private_key'])
        self.symmetric_sys.serealization_symmetric_key(
            encrypted_symmetric_key, self.settings['symmetric_key'])

    def encryption_message(self) -> None:
        """
        Функция шифрования текста
        """
        private_key = self.asymmetric_sys.get_private_key(
            self.settings['private_key'])
        encrypted_symmetric_key = self.symmetric_sys.get_symmetric_key(
            self.settings['symmetric_key'])
        symmetric_key = self.asymmetric_sys.decryption_symmetric_key(
            private_key, encrypted_symmetric_key)
        self.symmetric_sys.symmetric_encryption(
            symmetric_key, self.settings['initial_file'],
            self.settings['encrypted_text'])

    def decryption_message(self) -> None:
        """
        Функция расшифрования текста
        """
        private_key = self.asymmetric_sys.get_private_key(
            self.settings['private_key'])
        encrypted_symmetric_key = self.symmetric_sys.get_symmetric_key(
            self.settings['symmetric_key'])
        symmetric_key = self.asymmetric_sys.decryption_symmetric_key(
            private_key, encrypted_symmetric_key)
        self.symmetric_sys.symmetric_decryption(
            symmetric_key, self.settings['encrypted_text'],
            self.settings['decrypted_text'])
