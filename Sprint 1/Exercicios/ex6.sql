/*

    Apresente a query para listar o autor com maior número de livros publicados. 
    O resultado deve conter apenas as colunas codautor, nome, quantidade_publicacoes.

*/

SELECT 
    a.codAutor, 
    a.nome, 
    COUNT(l.cod) AS quantidade_publicacoes
FROM 
    autor a
JOIN 
    livro l ON a.codautor = l.autor
GROUP BY 
    a.codAutor, a.nome
ORDER BY 
    quantidade_publicacoes DESC
LIMIT 1;