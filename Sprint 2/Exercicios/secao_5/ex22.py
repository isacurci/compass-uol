from functools import reduce

def calcula_saldo(lancamentos) -> float:
    # continue este código
    valores = map(lambda x: x[0] if x[1] == 'C' else -x[0], lancamentos)
    return reduce(lambda acc, val: acc + val, valores)

# --- Adicione o código abaixo para testar a função e ver um retorno ---

if __name__ == "__main__":
    # Exemplo de lançamentos (igual ao do enunciado da imagem image_01e9af.png)
    meus_lancamentos = [
        (300, 'D'),
        (500, 'C'),
        (100, 'C')
    ]

    # Chama a função calcula_saldo com os lançamentos de exemplo
    saldo_final = calcula_saldo(meus_lancamentos)

    # Imprime o saldo final
    print(f"O saldo final é: {saldo_final}")

    # Outro exemplo para testar:
    lancamentos_2 = [
        (100.50, 'C'),
        (50.00, 'D'),
        (25.75, 'C')
    ]
    saldo_final_2 = calcula_saldo(lancamentos_2)
    print(f"O segundo saldo final é: {saldo_final_2}")