import random

# Passo 1: Declarar e inicializar a lista com 250 inteiros aleatórios
numeros = [random.randint(0, 1000) for _ in range(250)]

# Passo 2: Aplicar o método reverse
numeros.reverse()

# Passo 3: Imprimir o resultado
print(numeros)