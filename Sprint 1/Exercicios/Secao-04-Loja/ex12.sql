/*
 
	Apresente a query para listar código, 
	nome e data de nascimento dos dependentes do vendedor 
	com menor valor total bruto 
	em vendas (não sendo zero). 
	As colunas presentes no resultado devem ser cddep, 
	nmdep, dtnasc e valor_total_vendas.
	Observação: Apenas vendas com status concluído

*/

WITH total_vendas_por_vendedor AS (
    SELECT 
        cdvdd,
        SUM(qtd * vrunt) AS valor_total_vendas
    FROM tbvendas
    WHERE TRIM(LOWER(status)) LIKE '%conclu%'
    GROUP BY cdvdd
    HAVING valor_total_vendas > 0
),
vendedor_min_venda AS (
    SELECT cdvdd, valor_total_vendas
    FROM total_vendas_por_vendedor
    ORDER BY valor_total_vendas ASC
    LIMIT 1
)
SELECT 
    d.cddep,
    d.nmdep,
    d.dtnasc,
    v.valor_total_vendas
FROM tbdependente d
JOIN vendedor_min_venda v ON d.cdvdd = v.cdvdd;