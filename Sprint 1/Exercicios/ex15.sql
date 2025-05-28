/*

    Apresente a query para listar os códigos das vendas identificadas como deletadas. 
    Apresente o resultado em ordem crescente.

*/

SELECT cdven
FROM tbvendas
WHERE  deletado  != 0 
ORDER BY cdven ASC;
