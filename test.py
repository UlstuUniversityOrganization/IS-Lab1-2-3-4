import numpy as np
import random

class SubstitutionCipher():
    def __init__(self, substitution_table):
        self.substitution_table = substitution_table
        self.inv_substitution_table = {v: idx for idx, v in enumerate(substitution_table)}

    def encrypt(self, block):
        return bytes([self.substitution_table[b] for b in block])
    
    def decrypt(self, block):
        return bytes([self.inv_substitution_table[b] for b in block])


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
                block = block.ljust(self.block_size, b'\0')

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

# Example substitution table (simple example)
substitution_table = list(range(256))  # Identity for simplicity
random.shuffle(substitution_table)
# You can modify this table to create a real substitution cipher

# Create the substitution cipher and block cipher in CBC mode
substitution_cipher = SubstitutionCipher(substitution_table)
block_cipher_cbc = BlockCipherCBC(substitution_cipher)

# plaintext = [1, 2, 3, 4, 5, 6]
# print("plaintext: ", bytes(plaintext))
# iv = bytes([0] * 6)

# encrypted = block_cipher_cbc.encrypt(plaintext, iv)
# print("ciphertext: ", encrypted)

# decrypted = block_cipher_cbc.decrypt(encrypted, iv)

# print("decrypted: ", decrypted)


# Example usage
plaintext = b"Hello, world! This is a test."

print("Plaintext: ", plaintext)

iv = bytes([0] * 6)  # Initialization vector (IV) of block size

# Encrypt
ciphertext = block_cipher_cbc.encrypt(plaintext, iv)
print("Ciphertext:", ciphertext)

# Decrypt
decrypted = block_cipher_cbc.decrypt(ciphertext, iv)
print("Decrypted:", decrypted)  # Remove padding
# print("Decrypted:", decrypted.decode().rstrip('\x00'))  # Remove padding
