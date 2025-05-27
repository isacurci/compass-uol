/*

  Apresente a query para listar a quantidade de livros publicada por cada autor. 
  Ordenar as linhas pela coluna nome (autor), em ordem crescente.
  Além desta, apresentar as colunas codautor, nascimento e quantidade (total de livros de sua autoria).
  Dica para ordenação: Utilize Replace

*/

SELECT
  a.nome,
  a.codautor,
  a.nascimento,
  COUNT(l.cod) AS quantidade
FROM autor a
LEFT JOIN livro l ON a.codautor = l.autor
GROUP BY a.codautor
ORDER BY 
  REPLACE(
    REPLACE(a.nome, 'Á', 'A'),
    'á', 'a')