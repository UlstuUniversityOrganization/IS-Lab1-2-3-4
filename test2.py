def bbs(p, q, seed, length):
    N = p * q
    x = seed ** 2 % N
    result = []
    
    for _ in range(length):
        x = x ** 2 % N
        result.append(x % 2)  # Используем младший бит
    
    return result

# Пример использования
p = 383  # Пример простого числа
q = 503  # Пример простого числа
seed = 217  # Начальное значение (seed)
length = 10  # Длина последовательности

bbs_sequence = bbs(p, q, seed, length)
print(bbs_sequence)
