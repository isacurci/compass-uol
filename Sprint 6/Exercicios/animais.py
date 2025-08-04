# Passo 1: Declarar e inicializar a lista com 20 nomes de animais
animais = [
    "cachorro", "gato", "macaco", "urso", "lobo", "urubu", "aranha", "camelo",
    "pinguim", "corvo", "boi", "cavalo", "polvo", "água-viva", "tubarão", "lebre",
    "golfinho", "baleia", "lebre", "tartaruga"
]

# Passo 2: Ordenar em ordem crescente
animais.sort()

# Passo 3: Iterar e imprimir (usando list comprehension para imprimir)
print([f"Animal: {animal}" for animal in animais])

# Passo 4: Armazenar em um arquivo de texto
with open("animais.txt", "w", encoding="utf-8") as arquivo:
    for animal in animais:
        arquivo.write(f"{animal}\n")

print("\nNomes dos animais salvos em 'animais.txt'")