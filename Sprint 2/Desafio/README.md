## Etapas

### 1. **Carregar o Dataset**

A primeira etapa do projeto é carregar o dataset. O arquivo `.csv` contém informações sobre os aplicativos, como nome, categoria, classificações, avaliações, e outros dados.

### 2. **Remover Linhas Duplicadas**

Após carregar o dataset, removi as linha duplicadas.

### 3. **Limpeza de Dados - Installs**

A coluna **`Installs`** contém valores não numéricos, como símbolos de `+` e vírgulas `,`. Esses caracteres foram removidos para que possamos realizar análises numéricas.

### 4. **Análise de Top 5 Apps por Instalações**

Nesta etapa, usamos o método **`nlargest()`** para identificar os 5 aplicativos com o maior número de instalações.

### 5. **Análise de Categorias de Apps**

Geramos um gráfico de pizza para visualizar a distribuição das categorias de aplicativos na Play Store.

### 6. **Encontre o App Mais Caro**

Encontrar o aplicativo com o maior preço na Play Store.

### 7. **Contagem de Apps com a Classificação 'Mature 17+'**

Aqui contei quantos aplicativos possuem a classificação **'Mature 17+'**.

### 8. **Top 10 Apps por Número de Reviews**

Selecionamos os 10 aplicativos com mais reviews e geramos um gráfico para visualização.

### 9. **Cálculos sobre o Dataset**

Realizamos alguns cálculos sobre o dataset, como a média de reviews e a média de preços dos aplicativos.

### 10. **Gráficos de Análise Adicional**

Geramos gráficos adicionais para análise, como o preço médio por categoria e um gráfico de dispersão entre instalações e preço.

#### Preço Médio por Categoria

#### Gráfico de Dispersão - Instalações vs Preço

## Conclusão

Este projeto fornece uma análise básica da Play Store, incluindo insights sobre a distribuição de categorias, a popularidade dos aplicativos e o preço médio. O uso de gráficos ajuda a visualizar as informações de maneira clara e eficaz.
