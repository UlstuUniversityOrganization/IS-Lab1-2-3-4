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
    def __init__(self, generator):
        self.generator = generator
        # self.num_columns = num_columns

        substitution_table = list(range(2 ** 16))  # Identity for simplicity
        # substitution_table = list(range((2 ** 16) * self.num_columns))  # Identity for simplicity
        substitution_table = self.__shuffle(substitution_table, self.generator)

    

        self.substitution_table = substitution_table
        self.inv_substitution_table = {v: idx for idx, v in enumerate(self.substitution_table)}

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
        encrypted = b""
        for i in range(1, len(block), 2):
            idx = block[i - 1] + block[i] * 256
            encrypted_bytes = self.substitution_table[idx].to_bytes(2, byteorder='big')
            encrypted += encrypted_bytes

        return encrypted
    
    def decrypt(self, block): 
        encrypted = b""
        for i in range(1, len(block), 2):
            value = int.from_bytes(bytes([block[i - 1], block[i]]))
            original_value = self.inv_substitution_table[value]

            x = original_value % 256
            y = original_value // 256
            
            encrypted += bytes([x, y])

        return encrypted
        # return bytes([self.inv_substitution_table[b] for b in block])


class BlockCipherCBC():
    def __init__(self, substitution_cipher, block_size=6):
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
            block_to_encrypt = self.xor_bytes(block, prev_block)
            # Apply substitution
            encrypted_block = self.substitution_cipher.encrypt(block_to_encrypt)
            encrypted += encrypted_block
            # Update previous block
            prev_block = encrypted_block
            
        return encrypted

    def decrypt(self, ciphertext, iv):
        decrypted = b""
        prev_block = iv
        
        for i in range(0, len(ciphertext), self.block_size):
            block = ciphertext[i:i + self.block_size]
            # Pad the block if it's smaller than the block size
            if len(block) < self.block_size:
                block = block.ljust(self.block_size, b'\0')

            # Apply substitution (this reverses the substitution)
            block_to_xor = self.substitution_cipher.decrypt(block)
            # XOR with the previous ciphertext block
            decrypted_block = self.xor_bytes(block_to_xor, prev_block)
            decrypted += decrypted_block
            # Update previous block
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
        matrix_cipher = SubstitutionCipher(BbsGenerator(key))
        cipher = BlockCipherCBC(matrix_cipher)
        
        iv = b'\x00' * 6
        encrypted = cipher.encrypt(plaintext, iv)
        self.result_text.setText(f"{encrypted.hex()}")

    def decrypt_data(self):
        password = self.password_input.text().encode()
        md4 = SHA256()
        md4.update(password)
        key = int(md4.hexdigest(), 6*6) & 0xFFFFFFFF
        matrix_cipher = SubstitutionCipher(BbsGenerator(key))
        cipher = BlockCipherCBC(matrix_cipher)
        
        try: 
            ciphertext = bytes.fromhex(self.result_text.toPlainText())
        except:
            QMessageBox.critical(self, "Ошибка", "Не удалось расшифровать - данные не являются зашифрованным текстом.")
            return
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
