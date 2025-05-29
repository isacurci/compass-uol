# Instruções

Neste arquivo você apresentará suas entregas referentes ao desafio. Utilize o diretório "Desafio" para organizar seus artefatos e este README.md para fazer referência aos arquivos de código-fonte e demais entregáveis solicitados.

Esperamos que haja, minimamente:

- Passo a passo para obter o resultado entregue do desafio.
- Trechos de códigos e suas explicações.
- Relacionamento com a pasta de evidências (imagens).


# Etapas


1. ... [Etapa I](etapa-1)

    Nessa etapa dei início ao modelo relacional lógico, comecei olhando o que tinhamos no banco disponibilizado e fui criando as tabelas no MySQL Workbench.
    Foi uma etapa mais tranquila, pois já tinha feito antes, comecei a organizar as tabelas, separar as PKs e FKs.
    Como pode se ver em abaixo:

    ![amostra](../Evidencias/desafio0.png)

    ![amostra](../Evidencias/desafio1.png)

    ![amostra](../Evidencias/desafio2.png)

    Depois de criado as tabelas com suas respectivas FKs, PKs e relacionamentos entre si, exportei o código SQL e fiz algumas mudanças evidenciado em:

    ![amostra](../Evidencias/desafio3.png)

    Logo após rodei os scrips e criei as tabelas, evidenciado em:

    ![amostra](../Evidencias/desafio4.png)

    ## 📦 Resultado Final - Relacional

    O resultado final do desafio (modelagem relacional e dimensional, incluindo as views criadas) está disponível na pasta [etapa-1](../Desafio/etapa-1).

    ![amostra](../Desafio/etapa-1/modelo-relacional.png)


2. ... [Etapa 2](etapa-2)

    Dei inicio a modelagem dimensional, algo que nunca tinha estudado antes, comecei separando as tabelas dimensão e fato, conforme o vídeo de explicação do desafio, após ter estudado esse modelo e assistido o vídeo do Alex, sobre seu projeto de Data Warehouse no Youtube. Também conversei com o monitor Daniel, sobre algumas dúvidas na tabela Dim_tempo. Comecei a relacionar as tabelas e criá-las como pode evidenciar em:

    ![amostra](../Evidencias/desafio5.png)

    Após isso, tive que fazer os scritps de criação das VIEWS, criei as Views e conferi se tudo estava correto.

    ![amostra](../Evidencias/desafio6.png)