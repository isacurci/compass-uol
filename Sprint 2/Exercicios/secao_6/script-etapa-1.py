def split_csv_line(line):
    parts = []
    current = ''
    inside_quotes = False

    for char in line:
        if char == '"' and not inside_quotes:
            inside_quotes = True
        elif char == '"' and inside_quotes:
            inside_quotes = False
        elif char == ',' and not inside_quotes:
            parts.append(current.strip())
            current = ''
        else:
            current += char
    parts.append(current.strip())
    return parts

with open("actors.csv", "r", encoding="utf-8") as f:
    lines = f.readlines()

max_movies = 0
top_actor = ""

for line in lines[1:]:
    parts = split_csv_line(line.strip())
    
    try:
        name = parts[0].strip().strip('"')
        num_movies = int(parts[2].strip())
        
        if num_movies > max_movies:
            max_movies = num_movies
            top_actor = name

    except Exception as e:
        print("Erro ao converter:", parts)

print(f"O ator que mais possui filmes no dataset é {top_actor} com {max_movies} filmes.")
