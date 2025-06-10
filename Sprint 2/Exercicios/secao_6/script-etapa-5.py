def parse_csv_line(line):
    parts = []
    current_field = []
    in_quote = False
    
    i = 0
    while i < len(line):
        char = line[i]
        
        if char == '"':
            in_quote = not in_quote
        elif char == ',' and not in_quote:
            parts.append("".join(current_field))
            current_field = []
        else:
            current_field.append(char)
        i += 1
            
    parts.append("".join(current_field))
    
    final_parts = []
    for part in parts:
        stripped_part = part.strip()
        if len(stripped_part) > 1 and stripped_part.startswith('"') and stripped_part.endswith('"'):
            final_parts.append(stripped_part[1:-1])
        else:
            final_parts.append(stripped_part)
            
    return final_parts

max_avg = 0.0
top_actor = ""
lines = [] 

try:
    with open("actors.csv", "r", encoding="utf-8") as f:
        lines = f.readlines()
except FileNotFoundError:
    print("Erro: O arquivo 'actors.csv' não foi encontrado no diretório.")
except Exception as e:
    print(f"Ocorreu um erro geral ao abrir ou ler o arquivo: {e}")

# --- Início da Etapa 3 (cálculo do ator com maior média) ---
print("\n--- Resultados da Etapa 3 ---")
for line in lines[1:]: 
    try:
        parts = parse_csv_line(line)
        
        if len(parts) >= 3: 
            name = parts[0]
            total_gross = float(parts[1])
            num_movies = int(parts[2])

            if num_movies > 0:
                avg = total_gross / num_movies

                if avg > max_avg:
                    max_avg = avg
                    top_actor = name
            # else:
                # print(f"Aviso: Linha com formato inesperado (menos de 3 colunas, ignorado): {line.strip()}")
                # pass 
                
    except Exception as ve:
        # print(f"Aviso: Erro ao processar linha (ignorado): {ve} para '{line.strip()}' (Partes: {parts if 'parts' in locals() else 'Não gerado'})")
        pass 

print(f"O ator com maior média de bilheteria por filme é {top_actor} com ${max_avg:.2f} milhões.")
# --- Fim da Etapa 3 ---


print("\n--- Resultados da Etapa 4 ---")
# --- Início da Etapa 4 ---
movie_counts = {}

for line in lines[1:]:
    try:
        parts = parse_csv_line(line)
        
        if len(parts) >= 5: # A coluna '#1 Movie' é a quinta coluna (índice 4)
            movie_name = parts[4].strip() 

            if movie_name: 
                movie_counts[movie_name] = movie_counts.get(movie_name, 0) + 1
        # else:
            # print(f"Aviso (Etapa 4): Linha sem '#1 Movie' esperado: {line.strip()}")

    except Exception as e:
        # print(f"Aviso (Etapa 4): Erro ao processar linha para contagem de filmes: {e} para '{line.strip()}'")
        pass 

sorted_movies = []
for movie, count in movie_counts.items():
    sorted_movies.append((movie, count))

sorted_movies.sort(key=lambda item: (-item[1], item[0]))

print("Contagem de Filmes de Maior Bilheteria por Ator")
print("--------------------------------------------------")
for movie, count in sorted_movies:
    vezes_str = "vez" if count == 1 else "vezes"
    print(f"O filme {movie} aparece {count} {vezes_str} no dataset.")
# --- Fim da Etapa 4 ---


print("\n--- Resultados da Etapa 5 ---")
# --- Início da Etapa 5 ---
actor_total_gross_list = []

for line in lines[1:]:
    try:
        parts = parse_csv_line(line)
        
        if len(parts) >= 2: 
            actor_name = parts[0].strip()
            total_gross_value = float(parts[1].strip()) 

            if actor_name: 
                actor_total_gross_list.append((actor_name, total_gross_value))
        # else:
            # print(f"Aviso (Etapa 5): Linha sem dados de ator/receita esperados: {line.strip()}")

    except Exception as e:
        # print(f"Aviso (Etapa 5): Erro ao processar linha para lista de atores por receita: {e} para '{line.strip()}'")
        pass 

actor_total_gross_list.sort(key=lambda item: item[1], reverse=True)


print("Lista de Atores Ordenada por Receita Bruta Total")
print("--------------------------------------------------")
for actor, gross in actor_total_gross_list:
    print(f"{actor} - ${gross:.2f} milhões")