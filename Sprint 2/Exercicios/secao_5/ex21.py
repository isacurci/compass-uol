from functools import reduce # Importado, mas não usado na função conta_vogais

def conta_vogais(texto: str) -> int:
    # A string de vogais para comparação (minúsculas, sem acento)
    vogais = "aeiou" 
    
    # Filtra os caracteres do texto que são vogais (convertidos para minúsculas)
    # e então conta quantos elementos resultaram do filtro.
    return len(list(filter(lambda c: c.lower() in vogais, texto)))

# --- Exemplo de uso ---
if __name__ == "__main__":
    print(f"Número de vogais em 'AWS': {conta_vogais('AWS')}") # Saída esperada: 1 (a)
    print(f"Número de vogais em 'Python': {conta_vogais('Python')}") # Saída esperada: 1 (o)
    print(f"Número de vogais em 'Compass': {conta_vogais('Compass')}") # Saída esperada: 2 (o, a)
    print(f"Número de vogais em 'UOL': {conta_vogais('UOL')}") # Saída esperada: 2 (u, o)
    