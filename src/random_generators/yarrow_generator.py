
# from src.random_generators.generator import Generator
# from Crypto.Cipher import DES
# from Crypto.Random import get_random_bytes
# import hashlib
# import time
# import os

# class YarrowGenerator(Generator):

#     def __init__(self, seed, pg, pt):
#         super().__init__(seed)
#         self.n = 64
#         self.k = 64
#         self.pg = pg
#         self.pt = pt
#         self.t = 0
#         self.c0 = get_random_bytes(int(self.k / 8))
#         self.c = self.c0
#         self.cur_pg = pg
#         self.cur_pt = pt

#         current_time = str(time.time())
#         num_processes = str(len(os.pids()))
#         random_data = str(os.urandom(16))

#         entropy_data = current_time + num_processes + random_data

#         self.v = hashlib.sha1(entropy_data.encode()).hexdigest()

#         # self.key = get_random_bytes(int(self.k / 8))
#         # Create a DES cipher object
#         # self.cipher = DES.new(self.key, DES.MODE_ECB)
        

#     def G(self):
#         self.c = (self.c + 1) % (2 ** self.n)
#         c_bytes = self.c.to_bytes(8, 'big')
#         encrypted_block = self.cipher.encrypt(c_bytes)
#         return encrypted_block
    
#     def H(self, s: str):
#         s_i = s.encode()
#         result = s_i

#         while len(result) * 8 < self.k:
#             s_i = hashlib.sha256(result).digest()
#             result += s_i
        
#         result_bits = ''.join(f'{byte:08b}' for byte in result)
#         return result_bits[:self.k]
    
#     def run(self, i):
#         if self.cur_pg == 0:
#             self.key = self.G(i)
#             self.cipher = DES.new(self.key, DES.MODE_ECB)
#             self.cur_pg = self.pg
        
#         if self.cur_pt == 0:
#             v0 = hashlib.sha1((self.v + str(self.t)).encode()).hexdigest()
            
#             vi_prev = v0
#             vi = 0
#             for i in range(1, self.t + 1):
#                 input_str = vi_prev + v0 + str(i)
#                 vi = hashlib.sha1(input_str.encode()).hexdigest()
#             vt = vi

#             input_str = vt + self.key
#             hash = hashlib.sha1(input_str.encode()).hexdigest()
#             self.key = self.H(hash)

#             self.c = Ek()

    
#     def Ek(self, c):
#         ciphertext = self.cipher.encrypt(c)
#         return ciphertext

#     def rand(self):
#         rnd_value = (self.a * self.rand_state ** 3 + self.b * self.rand_state ** 2 + self.c * self.rand_state + self.d)
#         rnd_value = rnd_value % self.m
#         self.rand_state = rnd_value
#         return rnd_value
    
#     #Кубический конгруэнтный генератор
#     @staticmethod
#     def generator_str():
#         return "Кубический конгруэнтный генератор"
    
#     @classmethod
#     def from_interface(cls):
#         seed = int(input("Введите seed: "))
#         a = int(input("Введите a: "))
#         b = int(input("Введите b: "))
#         c = int(input("Введите c: "))
#         d = int(input("Введите d: "))
#         m = int(input("Введите m: "))
#         cls_instance = cls(seed, a, b, c, d, m)
#         return cls_instance

        