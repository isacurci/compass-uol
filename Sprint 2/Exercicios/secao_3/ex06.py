# Implemente a função my_map(list, f) que recebe uma lista como primeiro argumento e uma função como segundo argumento. Esta função aplica a função recebida para cada elemento da lista recebida e retorna o resultado em uma nova lista.
# Teste sua função com a lista de entrada [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] e com uma função que potência de 2 para cada elemento.

def my_map(lista, f):
    resultado = []
    for elemento in lista:
        resultado.append(f(elemento))
    return resultado

# Função que eleva um número ao quadrado
def potencia_de_2(x):
    return x ** 2

# Lista de teste
entrada = [1,2,3,4,5,6,7,8,9,10]

# Usando a my_map com a função potencia_de_2
saida = my_map(entrada, potencia_de_2)

print(saida)
