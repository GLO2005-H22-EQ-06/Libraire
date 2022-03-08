create table if not exists Clients
(
    id_client  char(36)    not null,
    nom       varchar(20) not null,
    prenom    varchar(20),
    email     varchar(20),
    adresse   varchar(50),
    telephone char(11),
    PRIMARY KEY (id_client)
);

CREATE TABLE IF NOT EXISTS Produits(
    id_produit char(36) not null, #le uuid de python retourne 36 caracteres donc j'ai mis à 36
    prix double,
    quantity integer,
    PRIMARY KEY (id_produit)
);

CREATE TABLE IF NOT EXISTS Promotions(
    id_promotion char(36) not NULL,
    remise integer,
    date_debut datetime not null,
    date_fin datetime not null,
    PRIMARY KEY (id_promotion)
);

CREATE TABLE IF NOT EXISTS Appliquer(
    id_promotion char(36),
    id_produit char(36),
    prix_remise double,
    PRIMARY KEY (id_promotion, id_produit),
    FOREIGN KEY (id_promotion)
    REFERENCES Promotions(id_promotion)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
    FOREIGN KEY (id_produit)
    REFERENCES Produits(id_produit)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

CREATE TABLE Facturer(
    id_client char(36),
    id_produit char(36),
    id_facture char(36) not null,
    date_achat datetime not null,
    quantite integer,
    prix_total DOUBLE,
    FOREIGN KEY (id_produit)
    REFERENCES Produits(id_produit)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
    FOREIGN KEY (id_client)
    REFERENCES Clients(id_client)
    ON UPDATE CASCADE
    ON DELETE NO ACTION
);
DELIMITER //
CREATE PROCEDURE validate_uuid(
    IN in_uuid char(36)
)
    DETERMINISTIC
    NO SQL
BEGIN
    IF NOT (SELECT in_uuid REGEXP
                   '[[:alnum:]]{8,}-[[:alnum:]]{4,}-[[:alnum:]]{4,}-[[:alnum:]]{4,}-[[:alnum:]]{12,}') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'ID provided is not valid UUID format';
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE validate_email(
    IN in_email varchar(100)
)
    DETERMINISTIC
    NO SQL
BEGIN
    IF NOT (SELECT in_email REGEXP '^[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'E-mail address provided is not valild e-mail format';
    END IF;
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER validate_client_id
    BEFORE INSERT
    ON Clients
    FOR EACH ROW
BEGIN
    CALL validate_uuid(NEW.id_client);
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER validate_product_id
    BEFORE INSERT
    ON Produits
    FOR EACH ROW
BEGIN
    CALL validate_uuid(NEW.id_produit);
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER validate_facture_id
    BEFORE INSERT
    ON Facturer
    FOR EACH ROW
BEGIN
    CALL validate_uuid(NEW.id_facture);
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER validate_promotion_id
    BEFORE INSERT
    ON Promotions
    FOR EACH ROW
BEGIN
    CALL validate_uuid(NEW.id_promotion);
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER validate_client_email
    BEFORE INSERT
    ON Clients
    FOR EACH ROW
BEGIN
    CALL validate_email(New.email);
END//
DELIMITER ;







DROP TABLE Clients;
DROP TABLE Facturer