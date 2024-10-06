from abc import abstractmethod

class Generator():
    def __init__(self, seed: int):
        self.seed = seed
        self.rand_state = seed

    @abstractmethod
    def rand(self):
        pass

    @classmethod
    def from_interface(cls):
        seed = int(input("Введите сид генератора: "))
        print("")

        return cls(seed)

    def rand_seq(self, length):
        seq = []
        for i in range(length):
            value = self.rand()
            seq.append(value)
        return seq
    
    @staticmethod
    def generator_str():
        return "Название генератора не задано"
    
    @staticmethod
    def seq_to_bits(seq, bit_length=-1):
        bits = []
        for s in seq:
            if bit_length < 0:
                bin_str = bin(s)[2:]
            else:
                bin_str = format(s, f'0{bit_length}b')
            bits.append(bin_str)
        return bits
    
    @staticmethod
    def bits_to_seq(bit_seq):
        seq = []
        for s in bit_seq:
            num = int(s, 2)
            seq.append(num)
        return seq
    
    @staticmethod
    def print_seq(seq, end="\n"):
        for s in seq:
            print(s, end=" ")
        print("", end=end)
    
    @staticmethod
    def save_seq(seq, file_path):
        outputs_str = ""
        
        for s in seq:
            outputs_str += str(s) + "\n"

        with open(file_path, "w") as file:
            file.write(outputs_str)
    
    @staticmethod
    def load_seq(file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()
        
        seq = []
        for line in lines:  
            num = int(line, 2)
            seq.append(num)
        
        return seq
