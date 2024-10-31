from src.random_generators.fips_generator import FIPSGenerator
import numpy as np
import random

class SubstitutionCipher():
    def __init__(self, generator):
        self.generator = generator

        substitution_table = list(range(2 ** 16))  # Identity for simplicity
        substitution_table = self.__shuffle(substitution_table, self.generator)

        self.substitution_table = substitution_table
        self.inv_substitution_table = {v: idx for idx, v in enumerate(self.substitution_table)}

    def __shuffle(self, lst, rng, num_inversions=1000):
        random.seed(generator.rand_value())
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
# substitution_table = list(range(256))  # Identity for simplicity
# random.shuffle(substitution_table)
# You can modify this table to create a real substitution cipher

# Create the substitution cipher and block cipher in CBC mode


generator = FIPSGenerator(456)

substitution_cipher = SubstitutionCipher(generator)
block_cipher_cbc = BlockCipherCBC(substitution_cipher)

# plaintext = [1, 2, 3, 4, 5, 6]
# print("plaintext: ", bytes(plaintext))
# iv = bytes([0] * 6)

# encrypted = substitution_cipher.encrypt(plaintext)
# print("ciphertext: ", encrypted)

# decrypted = substitution_cipher.decrypt(encrypted)

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
