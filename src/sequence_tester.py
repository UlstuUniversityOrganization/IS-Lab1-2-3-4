import numpy as np

class SequenceTester():
    def __init__(self):
        self.threshold = 1.82138636

    # Оценка пропорции нулей и едениц в проверяемой последовательности
    def frequency_test(self, normal_sequence: np.ndarray): 
        s = np.abs(normal_sequence.sum()) / np.sqrt(len(normal_sequence))
        test_passed = s <= self.threshold
        return test_passed, s
    
    # Анализ количества цепочек в проверяемой последовательности, где цепочка - это непрерывная последовательность одинаковых бит
    def chain_test(self, sequence: np.ndarray):
        pi = 1 / len(sequence) * sequence.sum()
        Vn = 1
        for i in range(len(sequence) - 1):
            Vn += 1 if sequence[i] != sequence[i + 1] else 0
        s = abs(Vn + - 2 * len(sequence) * pi * (1 - pi)) / (2 * np.sqrt(2 * len(sequence)) * pi * (1 - pi))
        
        test_passed = s < self.threshold
        return test_passed, s

    # Оценка общего числа посещений определенного состояния при произвольном обходе кумулятивной суммы
    def random_excursions_variant_test(self, normal_sequence: np.ndarray):
        X = normal_sequence
        S = np.cumsum(X)

        S_prime = np.concatenate(([0], S, [0]))

        L = np.count_nonzero(S_prime == 0) - 1

        states = np.arange(-9, 10)
        state_counts = {state: np.count_nonzero(S_prime == state) for state in states if state != 0}

        Y_stats = {}
        for j in state_counts:
            numerator = abs(state_counts[j] - L)
            denominator = np.sqrt(2 * L * (4 * abs(j) - 2))
            Y_stats[j] = numerator / denominator

        test_passed = all(Y <= self.threshold for Y in Y_stats.values())

        return test_passed, Y_stats
    

    def test_sequence(self, sequence):
        normal_sequence = 2 * sequence - 1
        
        test_passed_1, s_1 = self.frequency_test(normal_sequence)
        print(f"Частотный тест:\n\tСостояние: {'пройден' if test_passed_1 else 'не пройден'}\n\tСтатистика: {s_1}")

        test_passed_2, s_2 = self.chain_test(sequence)
        print(f"Тест на последовательность одинаковых бит:\n\tСостояние: {'пройден' if test_passed_2 else 'не пройден'}\n\tСтатистика: {s_2}")

        test_passed_3, _ = self.random_excursions_variant_test(normal_sequence)
        print(f"Тест на произвольные отклонения:\n\tСостояние: {'пройден' if test_passed_3 else 'не пройден'}")