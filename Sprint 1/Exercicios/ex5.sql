SELECT DISTINCT a.nome
FROM autor a
JOIN livro l ON l.autor = a.codautor
JOIN editora ed ON l.editora = ed.codeditora
JOIN endereco en ON ed.endereco = en.codEndereco
WHERE NOT (
    en.pais = 'Brasil'
    AND en.estado IN ('PARANÁ', 'RIO GRANDE DO SUL', 'SANTA CATARINA')
)
ORDER BY a.nome ASC;
