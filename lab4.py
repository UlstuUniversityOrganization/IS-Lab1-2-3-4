import sys
import struct
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
from src.SHA256 import SHA256
from src.random_generators.fips_generator import FIPSGenerator
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
import numpy as np

# Матричное шифрование + режим CFB
class MatrixCipher():
    def __init__(self, generator, size_matrix=6):
        self.generator = generator
        self.block_size = size_matrix
    
    def reset(self):
        self.generator.rng_state = self.generator.seed

    def encrypt_block(self, block):
        # Применяем матричное шифрование (например, умножение на ключевую матрицу)
        key_matrix = [self.generator.rand_value() for i in range(self.block_size*self.block_size)]
        key_matrix = np.array(key_matrix).reshape((self.block_size, self.block_size))
        encrypted_block = np.dot(key_matrix, block) % 256
        return encrypted_block.flatten()

    def decrypt_block(self, block):
        # Для расшифровки требуется обратная матрица
        key_matrix = [self.generator.rand_value() for i in range(self.block_size*self.block_size)]
        key_matrix = np.array(key_matrix).reshape((self.block_size, self.block_size))
        inv_key_matrix = np.linalg.inv(key_matrix).astype(int) % 256
        decrypted_block = np.dot(inv_key_matrix, block) % 256
        return decrypted_block.flatten()

class BlockCipher():
    def __init__(self, matrix_cipher, block_size=6):
        self.block_size = block_size
        self.matrix_cipher = matrix_cipher

    def xor_bytes(self, a, b):
        return bytes([x ^ y for x, y in zip(a, b)])

    def encrypt(self, plaintext, iv):
        self.matrix_cipher.reset()
        encrypted = b""
        prev_block = iv
        
        for i in range(0, len(plaintext), self.block_size):
            block = plaintext[i:i + self.block_size]
            # Дополняем блок нулями, если он меньше размера блоков
            if len(block) < self.block_size:
                block = block + [0] * (self.block_size - len(block))

            # Шифруем предыдущий блок (или IV для первого блока)
            keystream = self.matrix_cipher.encrypt_block(np.frombuffer(prev_block, dtype=np.uint8).reshape((self.matrix_cipher.block_size, 1)))
            # XOR с текущим блоком
            encrypted_block = self.xor_bytes(block, keystream)
            encrypted += encrypted_block
            # Обновляем предыдущий блок
            prev_block = encrypted_block
            
        return encrypted

    def decrypt(self, ciphertext, iv):
        self.matrix_cipher.reset()
        decrypted = b""
        prev_block = iv
        
        for i in range(0, len(ciphertext), self.block_size):
            block = ciphertext[i:i + self.block_size]
            # Дополняем блок нулями, если он меньше размера блоков
            if len(block) < self.block_size:
                block = block.ljust(self.block_size, b'\0')

            # Шифруем предыдущий зашифрованный блок
            keystream = self.matrix_cipher.encrypt_block(np.frombuffer(prev_block, dtype=np.uint8).reshape((self.matrix_cipher.block_size, 1)))
            # XOR с текущим блоком
            decrypted_block = self.xor_bytes(block, keystream)
            decrypted += decrypted_block
            # Обновляем предыдущий блок
            prev_block = block
            
        return decrypted


# Графический интерфейс на PyQt
class CipherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Введите пароль для генерации ключа:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.encrypt_button = QPushButton("Зашифровать")
        self.decrypt_button = QPushButton("Дешифровать")
        self.load_button = QPushButton("Загрузить файл")
        self.save_button = QPushButton("Сохранить в файл")
        
        self.result_text = QTextEdit()

        self.encrypt_button.clicked.connect(self.encrypt_data)
        self.decrypt_button.clicked.connect(self.decrypt_data)
        self.load_button.clicked.connect(self.load_file)
        self.save_button.clicked.connect(self.save_file)

        layout.addWidget(self.label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.load_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.encrypt_button)
        layout.addWidget(self.decrypt_button)
        layout.addWidget(self.result_text)

        self.setLayout(layout)

    def encrypt_data(self):
        plaintext = list(map(lambda x: ord(x) % 256, self.result_text.toPlainText()))
        password = self.password_input.text().encode()
        md4 = SHA256()
        md4.update(password)
        key = int(md4.hexdigest(), 6*6) & 0xFFFFFFFF
        matrix_cipher = MatrixCipher(FIPSGenerator(key))
        cipher = BlockCipher(matrix_cipher)
        
        iv = b'\x00' * 6
        encrypted = cipher.encrypt(plaintext, iv)
        self.result_text.setText(f"{encrypted.hex()}")

    def decrypt_data(self):
        password = self.password_input.text().encode()
        md4 = SHA256()
        md4.update(password)
        key = int(md4.hexdigest(), 6*6) & 0xFFFFFFFF
        matrix_cipher = MatrixCipher(FIPSGenerator(key))
        cipher = BlockCipher(matrix_cipher)

        ciphertext = bytes.fromhex(self.result_text.toPlainText())
        iv = b'\x00' * 6
        decrypted = cipher.decrypt(ciphertext, iv)
        try:
            self.result_text.setText(f"{decrypted.decode()}")
        except:
            QMessageBox.critical(self, "Ошибка", "Не удалось расшифровать - неверный ключ.")

    def load_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Загрузить файл", "", "All Files (*)", options=options)
        if file_name:
            with open(file_name, 'r', encoding='utf-8') as file:
                self.result_text.setText(file.read())

    def save_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Сохранить файл", "", "All Files (*)", options=options)
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as file:
                file.write(self.result_text.toPlainText())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    cipher_app = CipherApp()
    cipher_app.show()
    sys.exit(app.exec_())
