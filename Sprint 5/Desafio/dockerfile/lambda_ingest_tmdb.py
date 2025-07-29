import requests
import os
import csv
import json
import boto3
from dotenv import load_dotenv
from datetime import datetime
import time

# Carrega as variáveis do arquivo .env
load_dotenv()

# Variáveis do .env
api_key = os.getenv('TMDB_API_KEY')

print("API KEY carregada:", api_key)

# Configurações do S3
S3_BUCKET_NAME = 'data-lake-isa1'
CAMADA_ARMAZENAMENTO = 'Raw'
ORIGEM_DADO = 'TMDB'
FORMATO_DADO = 'JSON'
ESPECIFICACAO_DADO = 'Movies'

def get_tmdb_id_from_imdb(imdb_id):
    url = f"https://api.themoviedb.org/3/find/{imdb_id}?api_key={api_key}&external_source=imdb_id"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['movie_results']:
            return data['movie_results'][0]['id']
        else:
            print(f"Nenhum resultado TMDB para IMDB ID {imdb_id}")
    else:
        print(f"Erro ao buscar TMDB ID para IMDB ID {imdb_id}: {response.status_code}")
    return None

def get_movie_from_tmdb(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=pt-BR"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao buscar filme TMDB {movie_id}: {response.status_code}")
        return None

def main():
    # Use o perfil SSO configurado (ex: datalake5)
    session = boto3.Session(profile_name='datalake5')
    s3_client = session.client('s3')

    data_processamento = datetime.now().strftime('%Y/%m/%d')
    arquivos = []

    with open('movies.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='|')
        for row in reader:
            imdb_id = row['id']
            tmdb_id = get_tmdb_id_from_imdb(imdb_id)
            time.sleep(0.3)
            if not tmdb_id:
                continue
            movie_data = get_movie_from_tmdb(tmdb_id)
            time.sleep(0.3)
            if movie_data:
                file_name = f"{tmdb_id}.json"
                s3_path = f"{CAMADA_ARMAZENAMENTO}/{ORIGEM_DADO}/{FORMATO_DADO}/{ESPECIFICACAO_DADO}/{data_processamento}/{file_name}"
                try:
                    s3_client.put_object(
                        Bucket=S3_BUCKET_NAME,
                        Key=s3_path,
                        Body=json.dumps(movie_data),
                        ContentType='application/json'
                    )
                    print(f"Arquivo {file_name} enviado para {s3_path}")
                    arquivos.append(s3_path)
                except Exception as e:
                    print(f"Erro ao enviar para S3: {e}")

    print({"arquivos_enviados": arquivos})

if __name__ == "__main__":
    main()