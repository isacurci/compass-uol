/*

    Apresente a query para listar as 5 editoras com mais livros na biblioteca.
    O resultado deve conter apenas as colunas quantidade, nome, estado e cidade. 
    Ordenar as linhas pela coluna que representa a quantidade de livros em ordem decrescente.
    
*/

SELECT 
    COUNT(l.cod) AS quantidade, 
    e.nome, 
    en.estado, 
    en.cidade
FROM livro l 
JOIN editora e ON l.editora = e.codEditora
JOIN endereco en ON e.endereco = en.codEndereco
GROUP BY e.nome, en.estado, en.cidade
ORDER BY quantidade DESC
LIMIT 5;
