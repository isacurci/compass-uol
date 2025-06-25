# Usar uma imagem oficial do Python
FROM python:3.9-slim-buster

# Definir o dir de trabalho dentro do contêiner
WORKDIR /app

# Copiar o script carguru.py para o dir de trabalho no contêiner
COPY carguru.py .

# Comando para executar o script Python quando o contêiner for iniciado
CMD ["python", "carguru.py"]