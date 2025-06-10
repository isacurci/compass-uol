def pares_ate(n: int):
    for i in range(2, n + 1, 2):
        yield i

# --- Bloco para testar com sáida ---
if __name__ == "__main__":
    # Exemplo 1: Pares até 10
    gerador_ex_1 = pares_ate(10)
    print("Pares até 10:")
    for par in gerador_ex_1:
        print(par)

    print("\n---")

    # Exemplo 2: Pares até 5
    gerador_ex_2 = pares_ate(5)
    print("Pares até 5:")
    for par in gerador_ex_2:
        print(par)

    print("\n---") 
    
    # Exemplo 3: Convertendo para lista para ver todos de uma vez
    print("Pares até 12 (como lista):", list(pares_ate(12)))