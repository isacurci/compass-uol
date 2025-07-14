import boto3
import pandas as pd
from io import StringIO

# === Conexão com o S3 ===
session = boto3.Session(profile_name='teste')  # perfil SSO configurado
s3 = session.client('s3')

bucket_name = 'isabellabucket123'
object_key = 'basedados.csv'

# === Leitura do arquivo CSV ===
csv_obj = s3.get_object(Bucket=bucket_name, Key=object_key)
body = csv_obj['Body'].read().decode('utf-8')
df = pd.read_csv(StringIO(body), sep=';')

# === Conversão de mês por extenso para número ===
meses_map = {
    'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4,
    'maio': 5, 'junho': 6, 'julho': 7, 'agosto': 8,
    'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12
}
df['Mês_Num'] = df['Mês'].str.lower().map(meses_map)

# === Criação da coluna de data ===
df['Data'] = pd.to_datetime(df['Ano'].astype(str) + '-' + df['Mês_Num'].astype(str) + '-01')

# === Manipulações obrigatórias ===

# 1. Cláusula com dois operadores lógicos: consumo em "São Paulo", ano 2023
filtro = (df['Cidade'] == 'São Paulo') & (df['Ano'] == 2023)
df_filtrado = df[filtro]

# 2. Função de agregação: soma de consumo por campus
agregado = df.groupby('Campus')['Quantidade em kWh'].sum().reset_index()

# 3. Função condicional: consumo alto (> 10000 kWh)
df['Consumo Alto'] = df['Quantidade em kWh'].apply(lambda x: 'Sim' if x > 10000 else 'Não')

# 4. Função de conversão: transformar kWh em MWh
df['Quantidade em MWh'] = df['Quantidade em kWh'] / 1000

# 5. Função de string: campus em letras maiúsculas
df['Campus_MAIUSCULO'] = df['Campus'].str.upper()

# === Resultados (prints) ===
print('\n--- Dados filtrados: São Paulo em 2023 ---')
print(df_filtrado)

print('\n--- Consumo total por campus (kWh) ---')
print(agregado)

print('\n--- DataFrame final ---')
print(df.head())
