from abc import abstractmethod

class Generator():
    def __init__(self, seed):
        self.seed = seed
        self.rng_state = seed

    @abstractmethod
    def rand(self):
        pass

    def rand_value(self, bits=32):
        return int("".join(list(map(str, self.rand_seq(bits)))), 2)

    @classmethod
    def from_interface(cls):
        seed = int(input("Введите сид генератора: "))
        print("")

        return cls(seed)

    @staticmethod
    def generator_str():
        return "Название генератора не задано"
    
    def rand_seq(self, length):
        return [self.rand() for i in range(length)]
    
    @staticmethod
    def save_seq(seq, file_path):
        with open(file_path, "w") as file:
            file.write("".join(seq))
    
    @staticmethod
    def load_seq(file_path):
        with open(file_path, "r") as file:
            seq = list(map(int, file.readline()))
        return seq