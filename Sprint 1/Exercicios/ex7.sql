/*

    Apresente a query para listar o nome dos autores com nenhuma publicação. 
    Apresentá-los em ordem crescente.

*/


SELECT 
    nome
FROM 
    autor
WHERE 
    codautor NOT IN (
        SELECT autor FROM livro
    )
ORDER BY 
    nome ASC;
