# Leia o arquivo person.json, faça o parsing e imprima seu conteúdo.

# Dica: leia a documentação do pacote json

import json

with open('person.json', 'r', encoding='utf-8') as arquivo:
    dados = json.load(arquivo)   # Faz o parsing do JSON para um objeto Python (dicionário, lista, etc)

print(dados)
