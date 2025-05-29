-- -----------------------------------------------------
-- Table Cliente
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Cliente` (
  `idCliente` INT NOT NULL,
  `nomeCliente` VARCHAR(45) NULL,
  `cidadeCliente` VARCHAR(45) NULL,
  `estadoCliente` VARCHAR(45) NULL,
  `paisCliente` VARCHAR(45) NULL,
  PRIMARY KEY (`idCliente`))

-- -----------------------------------------------------
-- Table Combustivel
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Combustivel` (
  `idCombustivel` INT NOT NULL,
  `tipoCombustivel` VARCHAR(45) NULL,
  PRIMARY KEY (`idCombustivel`))

-- -----------------------------------------------------
-- Table Carro
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Carro` (
  `idCarro` INT NOT NULL,
  `kmCarro` INT NULL,
  `classiCarro` VARCHAR(45) NULL,
  `marcaCarro` VARCHAR(45) NULL,
  `modeloCarro` VARCHAR(45) NULL,
  `anoCarro` VARCHAR(4) NULL,
  `idCombustivel` INT NOT NULL,
  PRIMARY KEY (`idCarro`),
  CONSTRAINT `idCombustivel`
    FOREIGN KEY (`idCombustivel`)
    REFERENCES `Combustivel` (`idCombustivel`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)

-- -----------------------------------------------------
-- Table Vendedor
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Vendedor` (
  `idVendedor` INT NOT NULL,
  `nomeVendedor` VARCHAR(45) NULL,
  `sexoVendedor` TINYINT NULL,
  `estadoVendedor` VARCHAR(45) NULL,
  PRIMARY KEY (`idVendedor`))

-- -----------------------------------------------------
-- Table Locacao
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `Locacao` (
  `idLocacao` INT NOT NULL,
  `idCliente` INT NULL,
  `idCarro` INT NULL,
  `dataLocacao` DATE NULL,
  `horaLocacao` TIME NULL,
  `qtdDiaria` INT NULL,
  `vlrDiaria` DECIMAL(10,2) NULL,
  `dataEntrega` DATE NULL,
  `horaEntrega` TIME NULL,
  `idVendedor` INT NULL,
  PRIMARY KEY (`idLocacao`),
  CONSTRAINT `idCliente`
    FOREIGN KEY (`idCliente`)
    REFERENCES `Cliente` (`idCliente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `idCarro`
    FOREIGN KEY (`idCarro`)
    REFERENCES `Carro` (`idCarro`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `idVendedor`
    FOREIGN KEY (`idVendedor`)
    REFERENCES `Vendedor` (`idVendedor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
