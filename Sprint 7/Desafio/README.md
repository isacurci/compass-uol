# Desafio Etapa 4 - Processamento de Dados com AWS Glue

## Visão Geral

Neste desafio, o objetivo foi implementar a camada Refined do data lake, aplicando modelagem dimensional aos dados de filmes utilizando AWS Glue e Apache Spark para preparar dados estruturados prontos para análise e visualização.

---

## Etapas Realizadas

### 1. **Modelagem de Dados da Camada Refined**
- Desenvolvi o modelo dimensional seguindo o padrão Star Schema com:
 - **Tabela Fato:** fact_movies (contendo métricas e chaves estrangeiras)
 - **Tabelas Dimensão:** dim_artists, dim_companies, dim_countries, dim_time
- Defini os tipos de dados adequados para cada campo baseado na estrutura real dos dados
- Criei o diagrama ERD documentando os relacionamentos entre as tabelas

### 2. **Desenvolvimento dos Jobs AWS Glue**
- **Configuração do Job:**
- Seguindo o lab de glue - nenhum impedimento aqui
 
- **Processamento implementado:**
 - Leitura dos dados da camada Trusted Zone
 - Transformação seguindo o modelo dimensional definido
 - Aplicação de regras de limpeza e estruturação

### 3. **Criação das Tabelas no Data Catalog**
- Configurei as tabelas no AWS Glue Data Catalog seguindo a modelagem dimensional
- Implementei particionamento adequado para melhor performance nas consultas
- Estruturei os dados no formato PARQUET para otimização de storage e consultas

### 4. **Processamento com Apache Spark**
- Utilizei PySpark para transformar os dados da camada Trusted para Refined
- Implementei job com origem nos dados da Trusted Zone e destino na Refined Zone
- Apliquei todas as transformações necessárias seguindo os princípios de modelagem multidimensional

### 5. **Validação dos Casos de Uso Analíticos**
Preparei a estrutura para responder às seguintes análises:
- Filmes de drama mais bem avaliados ao longo das décadas
- Evolução da duração dos filmes de drama ao longo do tempo
- Relação entre nota média e número de votos dos filmes
- Identificação dos filmes de drama mais longos e suas avaliações

---

## Estrutura dos Arquivos
- `job.py` – Script Glue para processamento da camada Refined
- `modelo-der.png` – Diagrama do modelo implementado


## Conclusão

Esta etapa foi fundamental para consolidar o conhecimento sobre modelagem dimensional e processamento de dados. A implementação da camada Refined utilizando AWS Glue e Apache Spark permitiu estruturar os dados seguindo melhores práticas de Data Warehousing, preparando uma base sólida para análises multidimensionais e visualizações futuras no QuickSight.