/*

    Apresente a query para listar os 10 produtos menos vendidos pelos canais de E-Commerce ou Matriz 
    (Considerar apenas vendas concluídas).  
    As colunas presentes no resultado devem ser 
    cdpro, nmcanalvendas, nmpro e quantidade_vendas.

*/

SELECT 
    v.cdpro,
    v.nmcanalvendas,
    v.nmpro,
    SUM(v.qtd) AS quantidade_vendas
FROM tbvendas v
WHERE TRIM(LOWER(v.status)) LIKE '%conclu%'
  AND TRIM(LOWER(v.nmcanalvendas)) IN ('ecommerce', 'matriz')
GROUP BY v.cdpro, v.nmcanalvendas, v.nmpro
ORDER BY quantidade_vendas ASC
LIMIT 10;
