# Escreva uma função que recebe como parâmetro uma lista e retorna 3 listas: a lista recebida dividida em 3 partes iguais. Teste sua implementação com a lista abaixo
# lista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

def dividir_lista_em_3(lista):
  
    # Divide uma lista em 3 partes aproximadamente iguais.
    # Args:
       # lista (list): A lista a ser dividida.
    # Returns:
       # tuple: Uma tupla contendo as três listas divididas.
  
    n = len(lista)
    # Calcula o tamanho aproximado de cada parte
    # Usamos divisão inteira (//) para garantir que as partes sejam inteiras
    tamanho_parte = n // 3
    
    # Calcula os pontos de corte
    # A primeira parte vai do início até o tamanho_parte
    # A segunda parte vai de tamanho_parte até 2 * tamanho_parte
    # A terceira parte vai de 2 * tamanho_parte até o final da lista (n)
    
    lista1 = lista[0:tamanho_parte]
    lista2 = lista[tamanho_parte:2 * tamanho_parte]
    lista3 = lista[2 * tamanho_parte:n] 

    return lista1, lista2, lista3

# Teste da implementação
lista_original = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

lista_parte1, lista_parte2, lista_parte3 = dividir_lista_em_3(lista_original)

# Modifique a linha abaixo para imprimir apenas as listas no formato esperado pelo teste
print(f"{lista_parte1} {lista_parte2} {lista_parte3}")

# Remova ou comente os exemplos adicionais e prints descritivos se eles não forem esperados pelo teste
# print("\nTestando com uma lista de tamanho 10:")
# lista_nao_divisivel = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# l1, l2, l3 = dividir_lista_em_3(lista_nao_divisivel)
# print(f"Lista original: {lista_nao_divisivel}")
# print(f"Primeira parte: {l1}")
# print(f"Segunda parte: {l2}")
# print(f"Terceira parte: {l3}")