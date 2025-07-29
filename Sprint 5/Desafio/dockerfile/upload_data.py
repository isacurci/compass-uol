import boto3
import os
from datetime import datetime
import requests

S3_BUCKET_NAME = 'data-lake-isa1'  
CAMADA_ARMAZENAMENTO = 'Raw'
FORMATO_DADO = 'CSV'

CSV_FILES = {
    'movies': 'movies.csv',
    'series': 'series.csv'
}

def upload_file_to_s3_data_lake(local_file_path, s3_bucket, s3_path, s3_object_name):
    try:
        s3_client = boto3.client('s3', region_name=os.environ.get('AWS_REGION', 'us-east-1'))
        print(f"Tentando subir '{local_file_path}' para 's3://{s3_bucket}/{s3_path}/{s3_object_name}'...")
        s3_client.upload_file(local_file_path, s3_bucket, f"{s3_path}/{s3_object_name}")
        print(f"SUCESSO: '{local_file_path}' carregado para 's3://{s3_bucket}/{s3_path}/{s3_object_name}'.")
        return True
    except Exception as e:
        print(f"ERRO ao subir '{local_file_path}': {e}")
        return False

if __name__ == '__main__':
    for key, filename in CSV_FILES.items():
        if not os.path.exists(filename):
            print(f"Criando arquivo de exemplo '{filename}'...")
            with open(filename, 'w') as f:
                f.write("id,titulo,ano\n")
                f.write(f"1,Teste {key.capitalize()} 1,2023\n")
                f.write(f"2,Teste {key.capitalize()} 2,2024\n")
            print(f"Arquivo '{filename}' criado.")

    data_processamento = datetime.now().strftime('%Y/%m/%d')

    for especificacao_dado, local_file_name in CSV_FILES.items():
        origem_dado = 'Local'
        s3_prefix_path = os.path.join(
            CAMADA_ARMAZENAMENTO,
            origem_dado,
            FORMATO_DADO,
            especificacao_dado.capitalize(),
            data_processamento
        )
        s3_object_name = local_file_name

        print(f"\n--- Processando {local_file_name} ---")
        if upload_file_to_s3_data_lake(local_file_name, S3_BUCKET_NAME, s3_prefix_path, s3_object_name):
            print(f"Upload de {local_file_name} finalizado.")
        else:
            print(f"Falha no upload de {local_file_name}. Verifique as mensagens de erro acima.")