# 🎬 Desafio Filmes e Séries - Gênero Drama

Este desafio tem como objetivo construir um Data Lake na AWS focado em filmes e séries do gênero **Drama**, utilizando dados estruturados provenientes de arquivos CSV e dados complementares extraídos da API do TMDB.

---

## 🔍 Exploração Inicial dos Dados

Os dados foram explorados com foco no gênero **Drama**, utilizando duas fontes principais:

- 📁 Arquivos CSV fornecidos contendo títulos, notas, gêneros e anos de lançamento.
- 🌐 API do TMDB, que fornece detalhes para o csv.

---

## ❓ Questões para Análise

Com base na exploração dos dados, as seguintes questões serão respondidas:

1. **Quais são os filmes de drama mais bem avaliados ao longo das décadas?**
    >Base: genero = Drama
    >Filtro: notaMedia >= 7.5
    >Análise: Ver tendência temporal e quais títulos se destacam em cada década.

2. **Como a duração dos filmes de drama evoluiu ao longo do tempo e impacta na avaliação??**
    >Base: genero = 'Drama' 
    >Análise:Comparar tempo_minutos por década (ano_lancamento)
    Correlação: Filmes mais longos têm notas melhores ou piores?/ estão ficando mais longos ou mais curtos com o tempoo?
 
3. **Existe relação entre a nota média e a duração dos filmes de drama?**
    >Análise de correlação: Filmes mais longos tendem a ter nota mais alta ou mais baixa?

4. **TOP 5 Artistas em Filmes de Drama**
    >Análise: Identificar os 5 artistas com mais títulos
---

## Etapa 1: Coleta e Exploração Inicial dos Dados

Na primeira etapa, realizei o download dos dados brutos, criei a conta e comecei a consumir a API do TMDB. Utilizei o AWS CONFIGURE SSO para configurar igual na sprint anterior, rodei o conteiner no docker e igual na sprint anterior, 

- **Arquivos CSV:** Contendo informações básicas sobre filmes e séries, como títulos, notas, gêneros e anos de lançamento. 
- **API do TMDB:** Utilizada para enriquecer os dados dos filmes presentes nos CSVs. Foi primeiro gerada uma conta e uma chave no site fornecido e agregado ao script.

Após a coleta, foi feita uma exploração inicial para entender a estrutura dos dados, identificar possíveis inconsistências e definir os filtros necessários para focar no gênero Drama.

---

##  Etapa 2: Ingestão e Armazenamento no Data Lake

Na segunda etapa, foi desenvolvido um pipeline de ingestão automatizado:

- O script `lambda_ingest_tmdb.py` lê os IDs dos filmes a partir do arquivo `movies.csv`.
- Para cada ID, consulta a API do TMDB para obter informações detalhadas do filme.
- Os dados coletados são salvos em arquivos `.json`, organizados por data de processamento.
- Os arquivos `.json` são enviados automaticamente para o bucket S3 na AWS, estruturados em camadas e pastas conforme a arquitetura do Data Lake.

Essa automação garante que os dados estejam sempre atualizados e prontos para análises futuras, facilitando a governança e o acesso centralizado

---
# Conclusão

Apesar de alguns problemas que enfrentei essa semana, com problemas de saúde, tentei ao máximo resolver esse desafio. Tive dificuldades em configurar as credenciais, e com o runtime do lambda, mas ambos foram resolvidos com a ajuda do squad. Foi realizado também um teste para as credenciais em teste.py 