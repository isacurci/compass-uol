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
