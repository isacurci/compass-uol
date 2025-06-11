#Escreva um programa que lê o conteúdo do arquivo texto arquivo_texto.txt e imprime o seu conteúdo.
#Dica: leia a documentação da função open(...)

# Abre o arquivo em modo leitura
with open('arquivo_texto.txt', 'r', encoding='utf-8') as arquivo:
    conteudo = arquivo.read()

# Imprime o conteúdo do arquivo
print(conteudo, end='')
