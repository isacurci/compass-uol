/*

    Apresente a query para listar o código e nome cliente com maior gasto na loja.
    As colunas presentes no resultado devem ser cdcli, nmcli e gasto, 
    esta última representando o somatório das vendas (concluídas) atribuídas ao cliente.

*/

SELECT 
    cdcli,
    nmcli,
    ROUND(SUM(qtd * vrunt), 2) AS gasto
FROM tbvendas
WHERE TRIM(LOWER(status)) LIKE '%conclu%'
GROUP BY cdcli, nmcli
ORDER BY gasto DESC
LIMIT 1;
