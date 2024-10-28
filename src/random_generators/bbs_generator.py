from src.random_generators.generator import Generator
import sympy


class BbsGenerator(Generator):

    def __init__(self, seed, p=383, q=503):
        super().__init__(seed)

        assert p % 4 == 3
        assert q % 4 == 3
        assert sympy.isprime(p//2)
        assert sympy.isprime(q//2)

        self.a = p
        self.b = q
        self.N = p * q
        self.x = seed ** 2 % self.N

    def rand(self):
        self.x = self.x ** 2 % self.N
        return self.x % 2
    
    #Кубический конгруэнтный генератор
    @staticmethod
    def generator_str():
        return "Генератор BBS"
    
    @classmethod
    def from_interface(cls):
        # seed = int(input("Введите seed: "))
        # p = int(input("Введите p: "))
        # q = int(input("Введите q: "))

        # seed = 3
        # p = 11
        # q = 23
        
        seed = 8472
        p = 383
        q = 503
        
        # Sequence length that works: 1000

        cls_instance = cls(seed, p, q)
        return cls_instance

        