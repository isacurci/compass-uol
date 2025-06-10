def calcular_valor_maximo(operadores,operandos) -> float:
    
    def aplicar_operacao(op_e_par):
        op, (a, b) = op_e_par
        if op == '+':
            return a + b
        elif op == '-':
            return a - b
        elif op == '*':
            return a * b
        elif op == '/':
            return a / b
        elif op == '%':
            return a % b
        else:
            raise ValueError(f"Operador desconhecido: {op}")

    # Usa zip para juntar operador e par de operandos
    operacoes = zip(operadores, operandos)

    # Aplica cada operação com map e a função auxiliar
    resultados = map(aplicar_operacao, operacoes)

    # Retorna o máximo valor obtido
    return max(resultados)

# Exemplo
operadores = ['+','-','*','/','+']
operandos  = [(3,6), (-7,4.9), (8,-8), (10,2), (8,4)]

print(calcular_valor_maximo(operadores, operandos))  # Deve imprimir 12