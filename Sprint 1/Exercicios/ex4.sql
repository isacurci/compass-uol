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