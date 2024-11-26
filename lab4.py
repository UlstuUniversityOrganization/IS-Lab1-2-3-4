import sys
import struct
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
from src.SHA256 import SHA256
from src.random_generators.fips_generator import FIPSGenerator
from src.random_generators.bbs_generator import BbsGenerator
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel, QLineEdit, QMessageBox
from PyQt5.QtCore import Qt
import numpy as np
import random


class SubstitutionCipher():
    def __init__(self, generator, num_columns):
        self.generator = generator
        self.num_bytes = 2
        self.num_rows = (2 ** (self.num_bytes * 8))
        self.num_columns = num_columns
        
        # substitution_table = list(range(2 ** 16))  # Identity for simplicity
        substitution_table = list(range(self.num_rows * self.num_columns))  # Identity for simplicity
        substitution_table = self.__shuffle(substitution_table, self.generator) 

        self.substitution_table = substitution_table
        self.inv_substitution_table = {v: (idx % self.num_rows) for idx, v in enumerate(self.substitution_table)}

    def __shuffle(self, lst, rng, num_inversions=1000):
        random.seed(self.generator.rand_value())
        random.shuffle(lst)
        # # n = min(len(lst), num_inversions)
        # n = len(lst)
        # for i in range(n - 1, 0, -1):
        #     # Use the custom RNG to generate a random index for swapping
        #     j = generator.rand_value() % n
        #     lst[i], lst[j] = lst[j], lst[i]  # Swap in place
        return lst  # Now lst is shuffled in place

    def encrypt(self, block):
        
        # for i in range(1, len(block), 2):
        #     idx = block[i - 1] + block[i] * 256
        #     encrypted_bytes = self.substitution_table[idx].to_bytes(2, byteorder='big')
        #     encrypted += encrypted_bytes
        value = 0
        for i in range(0, len(block)):
            value = (value << 8) | block[i]
        encrypted_value = self.substitution_table[value + self.num_rows * random.randint(0, self.num_columns - 1)]
        encrypted = encrypted_value.to_bytes(self.num_bytes*self.num_columns, byteorder='big')

        return encrypted
    
    def decrypt(self, block): 
        # for i in range(1, len(block), 2):
        #     value = int.from_bytes(bytes([block[i - 1], block[i]]))
        #     original_value = self.inv_substitution_table[value]

        #     x = original_value % 256
        #     y = original_value // 256
            
        #     encrypted += bytes([x, y])

        value = int.from_bytes(block, byteorder='big')
        decrypted_row = self.inv_substitution_table[value]
        decrypted = b""

        for i in range(self.num_bytes):
            decrypted_value = decrypted_row & 0xFF
            decrypted_row = decrypted_row >> 8

            decrypted = bytes([decrypted_value]) + decrypted
        

        # for i in range(1, len(block)):
        #     value = int.from_bytes(bytes([block[i - 1], block[i]]))
        #     original_value = self.inv_substitution_table[value]

        #     x = original_value % 256
        #     y = original_value // 256
            
        #     decrypted += bytes([x, y])

        return decrypted
        # return bytes([self.inv_substitution_table[b] for b in block])


class BlockCipherCBC():
    def __init__(self, substitution_cipher, block_size=2):
        self.block_size = block_size
        self.substitution_cipher = substitution_cipher

    def xor_bytes(self, a, b):
        return bytes([x ^ y for x, y in zip(a, b)])

    def encrypt(self, plaintext, iv):
        encrypted = b""
        prev_block = iv
        
        for i in range(0, len(plaintext), self.block_size):
            block = plaintext[i:i + self.block_size]
            # Pad the block if it's smaller than the block size
            if len(block) < self.block_size:
                block = block + [0] * (self.block_size - len(block))

            # XOR the block with the previous ciphertext block
            
            # Apply substitution
            encrypted_block = self.substitution_cipher.encrypt(block)
            xored_block = self.xor_bytes(encrypted_block, prev_block)
            encrypted += xored_block
            # Update previous block
            prev_block = xored_block
            
        return encrypted

    def decrypt(self, ciphertext, iv):
        decrypted = b""
        prev_block = iv

        decryption_block_size = self.substitution_cipher.num_bytes * self.substitution_cipher.num_columns
        
        for i in range(0, len(ciphertext), decryption_block_size):
            block = ciphertext[i:i + decryption_block_size]
            # Pad the block if it's smaller than the block size
            if len(block) < decryption_block_size:
                block = block.ljust(decryption_block_size, b'\0')

            xored_block = self.xor_bytes(block, prev_block)
            
            # Apply substitution (this reverses the substitution)
            decrypted_block = self.substitution_cipher.decrypt(xored_block)
            # XOR with the previous ciphertext block
            # decrypted_block = self.xor_bytes(block_to_xor, prev_block)
            decrypted += decrypted_block
            # Update previous block
            prev_block = block
            
        return decrypted


# Графический интерфейс на PyQt
class CipherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.num_columns = 3
        

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
        matrix_cipher = SubstitutionCipher(BbsGenerator(key), self.num_columns)
        cipher = BlockCipherCBC(matrix_cipher)
        
        iv = b'\x00' * (matrix_cipher.num_bytes * matrix_cipher.num_columns)
        encrypted = cipher.encrypt(plaintext, iv)
        self.result_text.setText(f"{encrypted.hex()}")

    def decrypt_data(self):
        password = self.password_input.text().encode()
        md4 = SHA256()
        md4.update(password)
        key = int(md4.hexdigest(), 6*6) & 0xFFFFFFFF
        matrix_cipher = SubstitutionCipher(BbsGenerator(key), self.num_columns)
        cipher = BlockCipherCBC(matrix_cipher)
        
        try:
            ciphertext = bytes.fromhex(self.result_text.toPlainText())
        except:
            QMessageBox.critical(self, "Ошибка", "Не удалось расшифровать - данные не являются зашифрованным текстом.")
            return
        iv = b'\x00' * (matrix_cipher.num_bytes * matrix_cipher.num_columns)
        decrypted = cipher.decrypt(ciphertext, iv)
        try:
            self.result_text.setText(f"{decrypted.decode()}")
        except:
            QMessageBox.critical(self, "Ошибка", "Не удалось расшифровать - неверный ключ.\n\n Расшифрованный текст должен представлять из себя последовательность байт, формирующих текст в utf-8 кодировке. Однако, полученная последовательность байт не представляет из себя utf-8 кодировку.")

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
