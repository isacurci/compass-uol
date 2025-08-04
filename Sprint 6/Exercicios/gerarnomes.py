import random
import names
import os
import time

# Passo 3: Definição dos parâmetros
qtd_nomes_unicos = 39880
qtd_nomes_aleatorios = 10000000

# Passo 4: Definir a semente de aleatoriedade
random.seed(40)

# Passo 5: Gerar os nomes aleatórios
print(f"Gerando {qtd_nomes_unicos} nomes únicos...")
aux = []
for i in range(qtd_nomes_unicos):
    aux.append(names.get_full_name())

print(f"Gerando {qtd_nomes_aleatorios} nomes aleatórios...")
dados = []
for i in range(qtd_nomes_aleatorios):
    dados.append(random.choice(aux))

print("Geração de nomes concluída.")

# Passo 6: Gerar um arquivo de texto
nome_do_arquivo = "nomes_aleatorios.txt"
print(f"Salvando os nomes no arquivo '{nome_do_arquivo}'...")

with open(nome_do_arquivo, "w", encoding="utf-8") as arquivo:
    for nome in dados:
        arquivo.write(f"{nome}\n")

print(f"Arquivo '{nome_do_arquivo}' criado com sucesso.")

# Passo 7: Verificar o conteúdo (opcional, pode ser feito manualmente)
# print("\nConteúdo do arquivo 'nomes_aleatorios.txt' (primeiras 10 linhas):")
# with open(nome_do_arquivo, "r", encoding="utf-8") as arquivo:
#     for i in range(10):
#         print(arquivo.readline().strip())