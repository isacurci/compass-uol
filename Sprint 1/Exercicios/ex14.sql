/*

    Apresente a query para listar o gasto médio por estado da federação. 
    As colunas presentes no resultado devem ser estado e gastomedio. 
    Considere apresentar a coluna gastomedio arredondada na segunda casa decimal e ordenado de forma decrescente.
    Observação: Apenas vendas com status concluído.

*/

SELECT
    estado,
    ROUND(AVG(v.qtd * vrunt), 2) AS gastomedio
FROM tbvendas v
WHERE TRIM(LOWER(v.status)) LIKE '%conclu%'
GROUP BY estado
ORDER BY gastomedio DESC;
