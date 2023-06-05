import re

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton, QFileDialog)


class Window(QMainWindow):
    def __init__(self) -> None:
        """
        Функция инициализации окна и кнопок
        """
        super(Window, self).__init__()
        self.setWindowTitle('3DES')
        self.setFixedSize(600, 400)
        self.background = QLabel(self)
        self.background.setGeometry(0, 0, 600, 400)
        self.background.setPixmap(QPixmap("window.jpg").scaled(600, 400))
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
