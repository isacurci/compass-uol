# Usar uma imagem base oficial do Python
FROM python:3.9-slim-buster

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar o script mascarar_dados.py para o dir de trabalho no contêiner
COPY mascarar_dados.py .

# Comando padrão, mas que pode ser sobrescrito pelo "docker run"
CMD ["python", "mascarar_dados.py"]