from src.random_generators.generator import Generator
from src.random_generators.cubic_congruential_generator import CubicCongruentialGenerator
from src.random_generators.bbs_generator import BbsGenerator
from src.random_generators.standart_generator import StandartGenerator
import os
import numpy as np
from src.sequence_tester import SequenceTester

def generate_sequence():
    generators = [StandartGenerator, CubicCongruentialGenerator, BbsGenerator]
    for id, generator in enumerate(generators):
        print(f"{id + 1}. {generator.generator_str()}")
    generator_id = int(input("Выберите генератор: ")) - 1    
    generator_class = generators[generator_id]
    print("")

    generator = generator_class.from_interface()

    length = int(input("Введите длину последовательности: "))
    print("")

    seq = generator.rand_seq(length)

    return generator, length, seq


def load_sequence():
    path = input("Укажите путь до файла: ")
    print("")
    seq = Generator.load_seq(path)

    return None, len(seq), seq
    

if __name__ == "__main__":
    mode = ["Сгенерировать последовательность", "Загрузить последовательность из файла"]
    for idx, m in enumerate(mode):
        print(f"{idx + 1}. {m}")
    mode_id = int(input("Выберите вариант: ")) - 1
    print("")

    if mode_id == 0:
        generator, length, seq = generate_sequence()
    else:
        generator, length, seq = load_sequence()

    print(f"Двоичная последовательность:")
    print(f"{''.join(list(map(str, seq)))}\n")

    if mode_id == 0:
        path = r"data\seq.txt"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        Generator.save_seq("".join(list(map(str, seq))), path)

        print(f"Двоичная последовательность длиной {length} была сохранена по пути {path}")
    print("")

    print("Тестирование последовательностей:")
    tester = SequenceTester()
    tester.test_sequence(np.array(seq))
    print("------------------------------\n")
    
    