def parse_csv_line(line):
    parts = []
    current_field = []
    in_quote = False
    
    i = 0
    while i < len(line):
        char = line[i]
        
        if char == '"':
            in_quote = not in_quote
            # Não adiciona o caractere de aspas ao conteúdo do campo
        elif char == ',' and not in_quote:
            # Fim de um campo (vírgula fora das aspas)
            parts.append("".join(current_field))
            current_field = []
        else:
            current_field.append(char)
        i += 1
            
    # Adiciona o último campo
    parts.append("".join(current_field))
    
    # Processa cada parte: remove espaços em branco e aspas externas se presentes
    final_parts = []
    for part in parts:
        stripped_part = part.strip()
        # Verifica se o campo começa e termina com aspas e não é apenas um único caractere de aspas
        if len(stripped_part) > 1 and stripped_part.startswith('"') and stripped_part.endswith('"'):
            final_parts.append(stripped_part[1:-1]) # Remove as aspas
        else:
            final_parts.append(stripped_part)
            
    return final_parts

max_avg = 0.0
top_actor = ""
lines = [] # Inicializa lines para garantir que exista mesmo se o arquivo não for encontrado

try:
    with open("actors.csv", "r", encoding="utf-8") as f:
        lines = f.readlines()
except FileNotFoundError:
    print("Erro: O arquivo 'actors.csv' não foi encontrado no diretório.")
except Exception as e:
    print(f"Ocorreu um erro geral ao abrir ou ler o arquivo: {e}")

# Itera sobre as linhas, começando da segunda (ignorando o cabeçalho)
# Isso só ocorrerá se 'lines' tiver conteúdo (ou seja, se o arquivo foi lido com sucesso)
for line in lines[1:]:
    try:
        parts = parse_csv_line(line)
        
        # Garante que temos o número esperado de partes antes de tentar acessar
        if len(parts) >= 3: # Precisamos de pelo menos Actor, Total Gross, Number of Movies
            name = parts[0]
            total_gross = float(parts[1])
            num_movies = int(parts[2])

            if num_movies > 0:
                avg = total_gross / num_movies

                if avg > max_avg:
                    max_avg = avg
                    top_actor = name
            else:
                print(f"Aviso: Linha com formato inesperado (menos de 3 colunas, ignorado): {line.strip()}")
                pass 

    except Exception as ve:
        pass 
    
print(f"O ator com maior média de bilheteria por filme é {top_actor} com ${max_avg:.2f} milhões.")