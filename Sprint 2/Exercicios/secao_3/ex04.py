# Escreva uma função que recebe uma lista e retorna uma nova lista sem elementos duplicados. Utilize a lista a seguir para testar sua função.
# ['abc', 'abc', 'abc', '123', 'abc', '123', '123']

def remove_duplicados(lista):
    nova_lista = []
    vistos = set()
    for item in lista:
        if item not in vistos:
            nova_lista.append(item)
            vistos.add(item)
    return nova_lista

# Lista de teste
dados = ['abc', 'abc', 'abc', '123', 'abc', '123', '123']

# Chama a função e imprime o resultado
print(remove_duplicados(dados))
