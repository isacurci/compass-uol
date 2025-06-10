#Você está recebendo um arquivo contendo 10.000 números inteiros, um em cada linha. Utilizando lambdas e high order functions, apresente os 5 maiores valores pares e a soma destes.

#Você deverá aplicar as seguintes funções no exercício:

#map
#filter
#sorted
#sum

#Seu código deverá exibir na saída (simplesmente utilizando 2 comandos `print()`):
#a lista dos 5 maiores números pares em ordem decrescente;

# Lê os números do arquivo
with open("number.txt", "r") as f:
    numeros = list(map(int, f.readlines()))

# Filtra pares, ordena decrescente e pega os 5 maiores
maiores_pares = sorted(
    filter(lambda x: x % 2 == 0, numeros), reverse=True
)[:5]

# Soma os 5 maiores pares
soma = sum(maiores_pares)

# Exibe resultados
print(maiores_pares)
print(soma)
