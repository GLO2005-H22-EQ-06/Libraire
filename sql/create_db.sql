use glo_2005_labs;

create table if not exists CLIENTS
(
    id_client  varchar(50)    not null,
    nom       varchar(50) not null,
    prenom    varchar(50),
    email     varchar(50) unique,
    adresse   varchar(200),
    telephone char(11),
    primary key (id_client)
);

CREATE TABLE IF NOT EXISTS LIVRES
(
    id_produit char(36) not null,
    ISBN char(13) NOT NULL,
    titre varchar(250) NOT NULL ,
    auteur varchar(600) NOT NULL ,
    langue varchar(5) NOT NULL ,
    editeur varchar(100),
    annee date,
    nbrepages integer,
     description varchar(2000),
    primary key (ISBN),
    foreign key (id_produit) references Produits(id_produit)
);

CREATE TABLE IF NOT EXISTS COMPTE
(
    identifiant varchar(20),
    motDePasse varchar(50),
    primary key (identifiant)
);

CREATE TABLE IF NOT EXISTS ORDINATEURS
(
    id_produit char(36) NOT NULL,
    marque varchar(250) NOT NULL,
    modele varchar(250) NOT NULL ,
    taille_ecran integer,
    processeur varchar(250) NOT NULL,
    resolultion integer,
    ram integer NOT NULL,
    stockage integer NOT NULL,
    autonomie integer,
    primary key (id_produit)
);

create table if not exists ASSOCIER
(
    identifiant char(50),
    id_client char(36),
    foreign key (identifiant)
    references compte(identifiant)
    on delete cascade
    on update cascade,
    foreign key (id_client)
    references clients(id_client)
    on delete cascade
    on update cascade

);

CREATE TABLE IF NOT EXISTS PRODUITS(
    id_produit char(36) not null,
    prix double,
    quantity integer,
    PRIMARY KEY (id_produit)
);

CREATE TABLE IF NOT EXISTS PROMOTIONS(
    id_promotion char(36) not NULL,
    remise integer,
    date_debut datetime not null,
    date_fin datetime not null,
    PRIMARY KEY (id_promotion)
);

CREATE TABLE IF NOT EXISTS APPLIQUER(
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

CREATE TABLE IF NOT EXISTS FACTURER(
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

CREATE TABLE IF NOT EXISTS EVALUER
(
    id_client char(36),
    id_produit char(36),
    note integer NOT NULL ,
    commentaire TEXT,
    date datetime,
    primary key (id_client, id_produit),
    foreign key (id_produit) REFERENCES Produits(id_produit)
        ON DELETE CASCADE
        ON UPDATE CASCADE ,
    foreign key (id_client) REFERENCES Clients(id_client)
        ON DELETE CASCADE
        ON UPDATE CASCADE
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
CREATE TRIGGER valider_note_evaluer
    BEFORE INSERT
    ON Evaluer
    FOR EACH ROW
BEGIN
    IF NEW.note < 0 or NEW.note > 5
    THEN SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'rate between 0 and 5';
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER check_evaluation_per_user
    BEFORE INSERT
    ON Evaluer
    FOR EACH ROW
BEGIN
    IF (SELECT COUNT(*)
        FROM Evaluer
        WHERE id_client = NEW.id_client) > 1
    THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Product already evaluated';
    END IF;
END //
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

DELIMITER //
CREATE TRIGGER valider_insertion_tuple_promotion
    BEFORE INSERT
    ON promotions
    FOR EACH ROW
begin
    IF NEW.date_debut > NEW.date_fin then
        signal sqlstate '45000' set message_text = 'La date de debut ne peut pas etre superieur à la date de fin ';
    end if ;
    IF NEW.remise > 100 THEN
        signal sqlstate '45000' set message_text = 'La remise ne peut pas exceder 100% ';
    end if;
    IF CURRENT_DATE > NEW.date_debut then
        signal sqlstate '45000' set message_text = 'La date de debut ne peut pas pas être inférieure à la date courrante';
    end if ;
end //
DELIMITER ;