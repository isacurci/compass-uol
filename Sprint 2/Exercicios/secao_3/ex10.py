# Escreva uma função que recebe uma string de números separados por vírgula e retorne a soma de todos eles. Depois imprima a soma dos valores.
# A string deve ter valor  "1,3,4,6,10,76"
# Importante: Esperamos que você utilize split() em seu código.

def soma_numeros_string(numeros_str):

    numeros = numeros_str.split(',')  # Divide a string em uma lista de strings de números
    soma = 0
    for num_str in numeros:
        soma += int(num_str)  # Converte cada string de número para inteiro e adiciona à soma
    return soma

# String de números fornecida
string_de_numeros = "1,3,4,6,10,76"

# Chama a função e imprime o resultado
resultado_soma = soma_numeros_string(string_de_numeros)

print(resultado_soma)