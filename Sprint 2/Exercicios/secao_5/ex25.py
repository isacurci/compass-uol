def maiores_que_media(conteudo: dict) -> list:
    # 1. Calcular a média dos preços
    # Verifica se o dicionário está vazio para evitar erro de divisão por zero
    if not conteudo:
        return []

    soma_precos = sum(conteudo.values())
    media_precos = soma_precos / len(conteudo)

    # 2. Filtrar produtos com valor acima da média
    produtos_filtrados = []
    for nome, preco in conteudo.items():
        if preco > media_precos:
            produtos_filtrados.append((nome, preco))

    # 3. Ordenar a lista de tuplas pelo preço (segundo elemento da tupla) em ordem crescente
    # A função sorted() retorna uma nova lista ordenada, sem modificar a original.
    # A chave lambda item: item[1] indica que a ordenação deve ser feita pelo segundo elemento da tupla (o preço).
    produtos_ordenados = sorted(produtos_filtrados, key=lambda item: item[1])

    return produtos_ordenados

# Exemplo de uso :
if __name__ == "__main__":
    conjunto_produtos_exemplo = {
        "arroz": 4.99,
        "feijão": 3.49,
        "macarrão": 2.99,
        "leite": 3.29,
        "pão": 1.99
    }

    resultado = maiores_que_media(conjunto_produtos_exemplo)
    print(resultado)
    # Saída esperada para o exemplo: [('feijão', 3.49), ('arroz', 4.99)]