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
    CAST(strftime('%Y%m%d%H%M', dataLocacao || horaLocacao) AS INTEGER) AS idTempo,
    dataLocacao AS data,
    horaLocacao AS hora,
    strftime('%Y', dataLocacao) AS ano,
    strftime('%m', dataLocacao) AS mes,
    strftime('%d', dataLocacao) AS dia
FROM tb_locacao

UNION

SELECT DISTINCT 
    CAST(strftime('%Y%m%d%H%M', dataEntrega || horaEntrega) AS INTEGER) AS idTempo,
    dataEntrega AS data,
    horaEntrega AS hora,
    strftime('%Y', dataEntrega) AS ano,
    strftime('%m', dataEntrega) AS mes,
    strftime('%d', dataEntrega) AS dia
FROM tb_locacao;

-- View de fato: Locação
drop view Fato_Locacao 
CREATE VIEW Fato_Locacao AS
SELECT 
    idLocacao,
    idCliente,
    idCarro,
    idVendedor,
    CAST(strftime('%Y%m%d%H%M', dataLocacao || horaLocacao) AS INTEGER) AS idTempoLocacao,
    CAST(strftime('%Y%m%d%H%M', dataEntrega || horaEntrega) AS INTEGER) AS idTempoEntrega,
    qtdDiaria,
    vlrDiaria
FROM tb_locacao;
