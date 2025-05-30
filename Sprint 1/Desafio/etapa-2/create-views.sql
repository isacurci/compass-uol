-- View de dimensão: Cliente
CREATE VIEW Dim_Cliente AS
SELECT DISTINCT 
    idCliente,
    nomeCliente,
    cidadeCliente,
    estadoCliente,
    paisCliente
FROM tb_locacao;

-- View de dimensão: Carro
CREATE VIEW Dim_Carro AS
SELECT DISTINCT 
    idCarro,
    kmCarro,
    classiCarro,
    marcaCarro,
    modeloCarro,
    anoCarro,
    tipoCombustivel
FROM tb_locacao;

-- View de dimensão: Vendedor
CREATE VIEW Dim_Vendedor AS
SELECT DISTINCT 
    idVendedor,
    nomeVendedor,
    sexoVendedor,
    estadoVendedor
FROM tb_locacao;

-- View de dimensão: Tempo (datas de locação e entrega)
CREATE VIEW Dim_Tempo AS
SELECT DISTINCT
    printf('%04d-%02d-%02d',
        substr(REPLACE(dataLocacao, '.', ''), 1, 4),
        substr(REPLACE(dataLocacao, '.', ''), 5, 2),
        substr(REPLACE(dataLocacao, '.', ''), 7, 2)
    ) AS data,

    horaLocacao AS hora,

    substr(REPLACE(dataLocacao, '.', ''), 1, 4) AS ano,
    substr(REPLACE(dataLocacao, '.', ''), 5, 2) AS mes,
    substr(REPLACE(dataLocacao, '.', ''), 7, 2) AS dia

FROM tb_locacao

UNION

SELECT DISTINCT
    printf('%04d-%02d-%02d',
        substr(REPLACE(dataEntrega, '.', ''), 1, 4),
        substr(REPLACE(dataEntrega, '.', ''), 5, 2),
        substr(REPLACE(dataEntrega, '.', ''), 7, 2)
    ) AS data,

    horaEntrega AS hora,

    substr(REPLACE(dataEntrega, '.', ''), 1, 4) AS ano,
    substr(REPLACE(dataEntrega, '.', ''), 5, 2) AS mes,
    substr(REPLACE(dataEntrega, '.', ''), 7, 2) AS dia

FROM tb_locacao;

-- View de fato: Locação

CREATE VIEW Fato_Locacao AS
SELECT 
    idLocacao,
    idCliente,
    idCarro,
    idVendedor,
    dataLocacao,
    qtdDiaria,
    vlrDiaria,
    horaLocacao
FROM tb_locacao;
