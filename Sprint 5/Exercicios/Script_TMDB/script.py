import requests
import pandas as pd
from IPython.display import display

# Substituir aqui pela minha chave
api_key = "MY KEY"

# URL com parâmetros
url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={api_key}&language=pt-BR"

# Fazendo requisição
response = requests.get(url)
data = response.json()

# Processando dados
filmes = []
for movie in data['results']:
    df = {
        'Título': movie['title'],
        'Data de lançamento': movie['release_date'],
        'Visão geral': movie['overview'],
        'Votos': movie['vote_count'],
        'Média de votos': movie['vote_average']
    }
    filmes.append(df)

# Criar DF
df = pd.DataFrame(filmes)
display(df)