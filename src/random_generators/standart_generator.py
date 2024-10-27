from src.random_generators.generator import Generator
import random

class StandartGenerator(Generator):
    def __init__(self, seed):
        super().__init__(seed)
        random.seed = seed

    def rand(self):
        return random.randint(0, 1)

    @staticmethod
    def generator_str():
        return "Стандартный генератор"