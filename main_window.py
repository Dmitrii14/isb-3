import re
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton, QFileDialog)
import sys
from task import Coding as co


class Window(QMainWindow):
    def __init__(self) -> None:
        """
        Функция инициализации окна и кнопок
        """
        super(Window, self).__init__()
        self.setWindowTitle('3DES')
        self.setFixedSize(600, 400)
        self.info = QLabel(self)
        self.info.setText("Выберите размер ключа")
        self.info.setGeometry(225, 20, 500, 50)
        self.message = QLabel(self)
        self.message.setGeometry(225, 250, 200, 50)
        self.button_keys = QPushButton('Сгенерировать ключи', self)
        self.button_keys.setGeometry(200, 100, 200, 50)
        self.button_keys.clicked.connect(self.generation_key)
        self.button_keys.hide()
        self.key_size = QtWidgets.QComboBox(self)
        self.key_size.addItems(["64 бит", "128 бит", "192 бит"])
        self.key_size.setGeometry(200, 50, 200, 50)
        self.key_size.activated[str].connect(self.on_activated)
        self.button_e = QPushButton('Зашифровать текст', self)
        self.button_e.setGeometry(200, 150, 200, 50)
        self.button_e.clicked.connect(self.encryption)
        self.button_e.hide()
        self.button_d = QPushButton('Расшифровать текст', self)
        self.button_d.setGeometry(200, 200, 200, 50)
        self.button_d.clicked.connect(self.decryption)
        self.button_d.hide()
        self.show()

    def on_activated(self, text: str) -> None:
        """
        Функция для присвоения размера ключа
        """
        self.size = int(re.findall('(\d+)', text)[0])
        self.info.setText("Сгенирируйте ключ")
        self.button_keys.show()

    def hidden(self) -> None:
        """
        Функция для проявления кнопок для шифрования и дешифрования после того, как ключ сгенерирован
        """
        self.button_d.show()
        self.button_e.show()

    def generation_key(self) -> None:
        """
        Функция генерации ключей
        """
        way = str(QFileDialog.getExistingDirectory(caption='Выбор директории'))
        self.key = co(self.size, way)
        self.key.generation_key()
        self.info.setText("Ключи сгенерированы")
        self.message.setText("Зашифруйте текст")
        self.hidden()

    def encryption(self) -> None:
        """
        Функция шифрования
        """
        way_e = str(QFileDialog.getOpenFileName(caption='Выберите файл для шифрования', filter='*.txt'))
        way_e = way_e.split('\'')[1]
        self.key.encryption(way_e)
        self.info.setText("Текст зашифрован")
        self.message.setText("Расшифруйте текст")

    def decryption(self) -> None:
        """
        Функция дешифорвания
        """
        way = self.key.decryption()
        self.info.setText("Текст расшифрован")
        self.message.setGeometry(120, 250, 600, 30)
        self.message.setText(way)


def program() -> None:
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    program()
