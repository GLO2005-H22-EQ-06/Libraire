use glo_2005_labs;
create table if not exists CLIENTS
(
    id_client varchar(50) not null,
    nom       varchar(50) not null,
    prenom    varchar(50),
    email     varchar(50) unique,
    adresse   varchar(200),
    telephone char(11),
    primary key (id_client)
);
CREATE TABLE IF NOT EXISTS LIVRES
(
    id_produit char(36) not null ,
    ISBN        char(13)     unique NOT NULL,
    titre       varchar(250) NOT NULL,
    auteur      varchar(600) NOT NULL,
    langue      varchar(5)   NOT NULL,
    editeur     varchar(100),
    annee       date,
    nbrepages   integer,
    description varchar(2000),
    primary key (id_produit),
    foreign key (id_produit) references PRODUITS(id_produit)
);
delimiter //
create trigger add_book
    before insert on LIVRES
    for each row
    begin
        insert into produits values (NEW.id_produit, rand()*200, floor(rand()*100));
    end//
delimiter ;

CREATE TABLE IF NOT EXISTS COMPTE
(
    identifiant varchar(20),
    motDePasse  varchar(50),
    primary key (identifiant)
);
CREATE TABLE IF NOT EXISTS ORDINATEURS
(
    id_produit   char(36)     NOT NULL,
    marque       varchar(250) NOT NULL,
    modele       varchar(250) NOT NULL,
    taille_ecran integer,
    processeur   varchar(250) NOT NULL,
    resolultion  integer,
    ram          integer      NOT NULL,
    stockage     integer      NOT NULL,
    autonomie    integer,
    primary key (id_produit)
);
create table if not exists ASSOCIER
(
    identifiant char(50),
    id_client   char(36),
    foreign key (identifiant) references compte (identifiant) on delete cascade on update cascade,
    foreign key (id_client) references clients (id_client) on delete cascade on update cascade
);
CREATE TABLE IF NOT EXISTS PRODUITS
(
    id_produit char(36) not null,
    prix       double,
    quantity   integer,
    PRIMARY KEY (id_produit)
);
CREATE TABLE IF NOT EXISTS PROMOTIONS
(
    id_promotion char(36) not NULL,
    remise       integer,
    date_debut   datetime not null,
    date_fin     datetime not null,
    PRIMARY KEY (id_promotion)
);
CREATE TABLE IF NOT EXISTS APPLIQUER
(
    id_promotion char(36),
    id_produit   char(36),
    prix_remise  double,
    PRIMARY KEY (id_promotion, id_produit),
    FOREIGN KEY (id_promotion) REFERENCES Promotions (id_promotion) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id_produit) REFERENCES Produits (id_produit) ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS FACTURER
(
    id_client  char(36),
    id_produit char(36),
    id_facture char(36) not null,
    date_achat datetime not null,
    quantite   integer,
    prix_total DOUBLE,
    PRIMARY KEY (id_facture),
    FOREIGN KEY (id_produit) REFERENCES Produits (id_produit) ON DELETE NO ACTION ON UPDATE CASCADE,
    FOREIGN KEY (id_client) REFERENCES Clients (id_client) ON UPDATE CASCADE ON DELETE NO ACTION
);
CREATE TABLE IF NOT EXISTS EVALUER
(
    id_client   char(36),
    id_produit  char(36),
    note        integer NOT NULL,
    commentaire TEXT,
    date        datetime,
    primary key (id_client, id_produit),
    foreign key (id_produit) REFERENCES Produits (id_produit) ON DELETE CASCADE ON UPDATE CASCADE,
    foreign key (id_client) REFERENCES Clients (id_client) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE PANIER
(
    id_client  char(36),
    id_produit char(36),
    qantity    INTEGER DEFAULT 0,
    PRIMARY KEY (id_client, id_produit),
    FOREIGN KEY (id_client) REFERENCES Clients (id_client)
);

DELIMITER //
CREATE PROCEDURE validate_uuid(IN in_uuid char(36)) DETERMINISTIC NO SQL
BEGIN
    IF NOT (
        SELECT in_uuid REGEXP '[[:alnum:]]{8,}-[[:alnum:]]{4,}-[[:alnum:]]{4,}-[[:alnum:]]{4,}-[[:alnum:]]{12,}'
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET
                MESSAGE_TEXT = 'ID provided is not valid UUID format';
    END IF;
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE validate_email(IN in_email varchar(100))
    DETERMINISTIC NO SQL
BEGIN
    IF NOT (
        SELECT in_email REGEXP '^[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$'
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET
                MESSAGE_TEXT = 'E-mail address provided is not valild e-mail format';
    END IF;
END //
DELIMITER ;


DELIMITER //
CREATE TRIGGER validate_client_id
    BEFORE
        INSERT
    ON Clients
    FOR EACH ROW
BEGIN
    CALL validate_uuid(NEW.id_client);
END //
DELIMITER ;


DELIMITER //
CREATE TRIGGER valider_note_evaluer
    BEFORE
        INSERT
    ON Evaluer
    FOR EACH ROW
BEGIN
    IF NEW.note < 0
        or NEW.note > 5 THEN
        SIGNAL SQLSTATE '45000'
            SET
                MESSAGE_TEXT = 'rate between 0 and 5';
    END IF;
END //
DELIMITER ;


DELIMITER //
CREATE TRIGGER check_evaluation_per_user
    BEFORE INSERT ON Evaluer
    FOR EACH ROW
BEGIN
    IF (
           SELECT COUNT(*)
           FROM Evaluer
           WHERE id_client = NEW.id_client
       ) > 1 THEN
        SIGNAL SQLSTATE '45000'
            SET
                MESSAGE_TEXT = 'Product already evaluated';
    END IF;
END //
DELIMITER ;


DELIMITER //
CREATE TRIGGER validate_product_id
    BEFORE INSERT ON Produits
    FOR EACH ROW
BEGIN
    CALL validate_uuid(NEW.id_produit);
END //
DELIMITER ;


DELIMITER //
CREATE TRIGGER validate_facture_id
    BEFORE
        INSERT
    ON Facturer
    FOR EACH ROW
BEGIN
    CALL validate_uuid(NEW.id_facture);
END //
DELIMITER ;


DELIMITER //
CREATE TRIGGER validate_promotion_id
    BEFORE INSERT ON Promotions
    FOR EACH ROW
BEGIN
    CALL validate_uuid(NEW.id_promotion);
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER validate_client_email
    BEFORE INSERT
    ON Clients
    FOR EACH ROW
BEGIN
    CALL validate_email(New.email);
END //

DELIMITER ;
DELIMITER //
CREATE TRIGGER valider_insertion_tuple_promotion
    BEFORE
        INSERT
    ON promotions
    FOR EACH ROW
begin
    IF NEW.date_debut > NEW.date_fin then
        signal sqlstate '45000'
            set
                message_text = 'La date de debut ne peut pas etre superieur à la date de fin ';
    end if;
    IF NEW.remise > 100 THEN
        signal sqlstate '45000'
            set
                message_text = 'La remise ne peut pas exceder 100% ';
    end if;
    IF CURRENT_DATE > NEW.date_debut then
        signal sqlstate '45000'
            set
                message_text = 'La date de debut ne peut pas pas être inférieure à la date courrante';
    end if;
end //
DELIMITER ;

DELIMITER //
CREATE TRIGGER update_inventory
    AFTER INSERT ON PANIER
    FOR EACH ROW
    BEGIN
        IF (select quantity from produits where PRODUITS.id_produit = NEW.id_produit) > NEW.quantity;
        THEN signal sqlstate  '45000' set Message_TEXT = 'Quantity insuffisante';
        End if;
        #UPDATE PRODUITS SET quantity = quantity - NEW.quantity WHERE id_produit = NEW.id_produit;
    end //
DELIMITER ;




DELIMITER //
CREATE TRIGGER verify_cart_before_insertion before insert on panier
    for each row
    begin
        declare old_product_quantity int;
        declare nbre_prod_present int;
        declare cart_product_quantity int;
        select quantity into old_product_quantity from produits where PRODUITS.id_produit = NEW.id_produit;
        select count(*) into nbre_prod_present from panier where id_produit = NEW.id_produit;
        select sum(quantity) into cart_product_quantity from panier where id_produit = NEW.id_produit;
        if (nbre_prod_present > 0)
        then
            call update_panier_quantity(NEW.id_client, NEW.id_produit, NEW.quantity);

        elseif (old_product_quantity < NEW.qantity) then
                signal sqlstate  '45000' set Message_TEXT = 'Quantity insufficient in stock';
        elseif (old_product_quantity > NEW.qantity) then
            insert into panier values (NEW.id_client, NEW.id_produit, new.qantity);
        end if;
    end //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE update_panier_quantity(in in_id_client char(36), in_id_produit char(36), inQuantity int)
begin
    declare quant int;
    select p.quantity into quant from panier p where id_client = in_id_client and id_produit = in_id_produit;
    update panier set quantity = quant + inQuantity where id_produit = in_id_produit and id_client = in_id_client;
end //
DELIMITER ;





select * from clients;

insert into produits value ('5f1cbc91-af0d-11ec-acf3-645d863fa25e', 10, 200);
insert into clients values ('ab2d0fc0-7224-11ec-8ef2-b658b885fb3e', 'foo', 'barr', 'mail@gmail.com', 'adrees', 11111111111);
insert into panier value ('ab2d0fc0-7224-11ec-8ef2-b658b885fb3e', '5f1cbc91-af0d-11ec-acf3-645d863fa25e', 150);

select * from produits;
select * from panier where id_client = 'ab2d0fc0-7224-11ec-8ef2-b658b885fb3e';

drop table panier;