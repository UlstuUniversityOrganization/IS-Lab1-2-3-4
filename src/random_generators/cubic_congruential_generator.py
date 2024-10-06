from src.random_generators.generator import Generator


class CubicCongruentialGenerator(Generator):

    def __init__(self, seed, a, b, c, d, m):
        super().__init__(seed)
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.m = m

    def rand(self):
        rnd_value = (self.a * self.rand_state ** 3 + self.b * self.rand_state ** 2 + self.c * self.rand_state + self.d)
        rnd_value = rnd_value % self.m
        self.rand_state = rnd_value
        return rnd_value
    
    #Кубический конгруэнтный генератор
    @staticmethod
    def generator_str():
        return "Кубический конгруэнтный генератор"
    
    @classmethod
    def from_interface(cls):
        seed = int(input("Введите seed: "))
        a = int(input("Введите a: "))
        b = int(input("Введите b: "))
        c = int(input("Введите c: "))
        d = int(input("Введите d: "))
        m = int(input("Введите m: "))
        cls_instance = cls(seed, a, b, c, d, m)
        return cls_instance

        