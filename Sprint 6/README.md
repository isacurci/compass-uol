# Resumo

Nesta sprint, avancei no desenvolvimento de habilidades em processamento de dados, focando no uso do **Apache Spark** com Python (PySpark) para manipulação de grandes volumes de dados. O objetivo foi aplicar conceitos de dataframes, comandos SQL e automação de tarefas, dando continuidade ao pipeline de dados iniciado nas sprints anteriores.

---
## 🎓 Cursos Realizados


### *Fundamentals of Analytics - 2*

### *AWS GLUE*

## 🚀 Exercicios

### 1. **Geração de Dados Aleatórios**
- Criação de um script Python para gerar um arquivo `nomes_aleatorios.txt` com 10 milhões de nomes únicos, simulando um grande volume de dados para análise.
- O script utiliza bibliotecas como `random` e listas auxiliares para garantir diversidade nos nomes.

### 2. **Processamento com PySpark**
- Configuração do Java 17 para garantir compatibilidade com o PySpark.
- Criação de um script Python (`apache_spark.py`) para:
  - Inicializar uma SparkSession.
  - Ler o arquivo `nomes_aleatorios.txt` como dataframe.
  - Realizar operações básicas de visualização e manipulação dos dados, como exibir as primeiras linhas e preparar o dataframe para análises futuras.

### 3. **Resolução de Problemas**
- Ajuste de variáveis de ambiente (`JAVA_HOME`, `PATH`) para garantir o funcionamento do Spark localmente.
- Testes e validação do ambiente, documentando eventuais erros e soluções encontradas durante a configuração.

---

## 🛠️ Principais Aprendizados

- Resolução de problemas: - Ajuste de variáveis de ambiente (`JAVA_HOME`, `PATH`) para garantir o funcionamento do Spark localmente.
- Prática com geração e manipulação de grandes volumes de dados em Python.
- Configuração do ambiente Spark local no Windows, incluindo integração com o Python e o Java.
- Uso do PySpark para leitura, transformação e análise inicial de dados em formato texto.

---

## 📂 Estrutura dos Arquivos

- `gerarnomes.py` – Script para geração do arquivo de nomes aleatórios.
- `nomes_aleatorios.txt` – Arquivo de dados gerado para análise.
- `apache_spark.py` – Script para leitura e manipulação dos dados com PySpark.

---

## 👩‍💻 Conclusão

Essa sprint foi fundamental para consolidar meus conhecimentos em processamento de dados com Apache Spark e reforçar a integração com serviços como o AWS Glue. A prática com geração e manipulação de dados me permitiu compreender melhor os processos de ETL e foram fundamentais para o desenvolvimento do desafio da Sprint.