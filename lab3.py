import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QFileDialog, QVBoxLayout, QWidget, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import QFileInfo
import struct
from src.random_generators.bbs_generator import BbsGenerator
from src.SHA256 import SHA256

# Основной класс интерфейса
class CryptoApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Шифрование с SHA256 и генератором случайных чисел")
        self.setGeometry(300, 300, 500, 400)

        self.layout = QVBoxLayout()

        self.label_password = QLabel("Введите пароль:")
        self.layout.addWidget(self.label_password)

        self.text_password = QLineEdit(self)
        #self.text_password.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.text_password)

        self.text_editor = QTextEdit(self)
        self.layout.addWidget(self.text_editor)

        self.button_load = QPushButton("Загрузить текст из файла", self)
        self.button_load.clicked.connect(self.load_from_file)
        self.layout.addWidget(self.button_load)

        self.button_encrypt = QPushButton("Зашифровать", self)
        self.button_encrypt.clicked.connect(self.encrypt_text)
        self.layout.addWidget(self.button_encrypt)

        self.button_decrypt = QPushButton("Расшифровать", self)
        self.button_decrypt.clicked.connect(self.decrypt_text)
        self.layout.addWidget(self.button_decrypt)

        self.button_save = QPushButton("Сохранить в файл", self)
        self.button_save.clicked.connect(self.save_to_file)
        self.layout.addWidget(self.button_save)

        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

    def hash_password(self, password):
        """Хеширование пароля с помощью SHA256"""
        sha256 = SHA256()
        sha256.update(password.encode('utf-8'))
        return sha256.hexdigest()

    def encrypt_text(self):
        """Шифрование текста"""
        password = self.text_password.text()
        if not password:
            self.text_editor.setText("Пароль не может быть пустым!")
            return

        hashed_password = self.hash_password(password)
        generator = BbsGenerator(int(hashed_password, 16))

        text = self.text_editor.toPlainText()
        encrypted_text = "".join(chr(ord(c) ^ generator.rand_value() % 256) for c in text)
        self.text_editor.setText(encrypted_text)

    def decrypt_text(self):
        """Дешифрование текста"""
        self.encrypt_text()  # Шифрование потоком случайных чисел двустороннее

    def save_to_file(self):
        """Сохранение зашифрованного текста в файл с указанием кодировки UTF-8"""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(self.text_editor.toPlainText())

    def load_from_file(self):
        """Загрузка текста из файла с указанием кодировки UTF-8"""
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Загрузить файл", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.text_editor.setPlainText(content)
            except UnicodeDecodeError:
                QMessageBox.critical(self, "Ошибка", "Не удалось загрузить файл. Некорректная кодировка.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CryptoApp()
    window.show()
    sys.exit(app.exec_())