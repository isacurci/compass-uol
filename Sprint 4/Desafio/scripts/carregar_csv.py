import boto3
import os

# Cria uma sessão com o perfil do AWS CLI configurado
session = boto3.Session(profile_name='teste')

# Cria um cliente S3 usando as credenciais do perfil SSO
s3 = session.client('s3')

# Nome do bucket S3 e caminho do arquivo
bucket_name = 'isabellabucket123'
file_name = r'C:\Users\isabe\Downloads\basedados.csv'
s3_object_name = 'basedados.csv'

# Verifique se o arquivo existe antes de tentar enviá-lo
if not os.path.isfile(file_name):
    print(f"Erro: O arquivo '{file_name}' não foi encontrado!")
else:
    try:
        # Envia o arquivo para o bucket S3
        s3.upload_file(file_name, bucket_name, s3_object_name)
        print(f"Arquivo '{file_name}' carregado com sucesso para '{bucket_name}' como '{s3_object_name}'.")
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
