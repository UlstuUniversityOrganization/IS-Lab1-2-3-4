from src.random_generators.generator import Generator
from src.random_generators.cubic_congruential_generator import CubicCongruentialGenerator
import os
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes

def generate_sequence():
    generators = [CubicCongruentialGenerator]
    for id, generator in enumerate(generators):
        print(f"{id + 1}. {generator.generator_str()}")
    generator_id = int(input("Выберите генератор: ")) - 1    
    generator_class = generators[generator_id]
    print("")

    generator = generator_class.from_interface()

    length = int(input("Введите длину последовательности: "))
    print("")

    seq = generator.rand_seq(length)
    bit_seq = Generator.seq_to_bits(seq)

    return generator, length, seq, bit_seq


def load_sequence():
    path = input("Укажите путь до файла: ")
    print("")
    seq = Generator.load_seq(path)
    bit_seq = Generator.seq_to_bits(seq)

    return None, len(seq), seq, bit_seq
    

if __name__ == "__main__":
    mode = ["Сгенерировать последовательность", "Загрузить последовательность из файла"]
    for idx, m in enumerate(mode):
        print(f"{idx + 1}. {m}")
    mode_id = int(input("Выберите вариант: ")) - 1
    print("")

    if mode_id == 0:
        generator, length, seq, bit_seq = generate_sequence()
    else:
        generator, length, seq, bit_seq = load_sequence()

    print("Последовательность в десятичных числах:")
    Generator.print_seq(seq)
    print("")

    print("Последовательность в двоичных числах:")
    Generator.print_seq(bit_seq)
    print("")

    if mode_id == 0:
        path = r"data\seq.txt"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        Generator.save_seq(bit_seq, path)

        print(f"Двоичная последовательность длиной {length} была сохранена по пути {path}")