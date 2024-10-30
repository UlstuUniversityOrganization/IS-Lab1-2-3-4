from src.random_generators.generator import Generator
import hashlib

class FIPSGenerator(Generator):
    def __init__(self, seed):
        q = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
        b = 160
        if b < 160 or b > 512:
            raise ValueError("Значение b должно быть в диапазоне от 160 до 512 бит.")
        
        self.s = seed % (2 ** b)

        self.t = 0x67452301efcdab8998badcfe10325476c3d2e1f0
        self.q = q
        self.b = b

        super().__init__(seed)
    
    
    @staticmethod
    def G(t, c, b):
        H = [
            t >> (128 - 32 * i) & 0xFFFFFFFF for i in range(5)
        ]

        M = c.to_bytes((b + 7) // 8, 'big') + b'\x00' * ((512 - b + 7) // 8)
        
        M_words = [int.from_bytes(M[i:i+4], 'big') for i in range(0, len(M), 4)]
        
        sha1 = hashlib.sha1()
        sha1.update(M)
        result = sha1.digest()

        return int.from_bytes(result, 'big')


    def rand(self):
        y_i = 0
        z_i = (self.s + y_i) % (2 ** self.b)
        x_i = FIPSGenerator.G(self.t, z_i, self.b) % self.q
        self.s = (1 + self.s + x_i) % (2 ** self.b)
        return x_i & 1
    

    @staticmethod
    def generator_str():
        return "Генератор FIPS-186"