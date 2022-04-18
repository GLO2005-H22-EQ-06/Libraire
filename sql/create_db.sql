select L.*, get_prix_remise(L.isbn) as prix_remise from LIVRES L order by nbrepages desc limit 50;
create table if not exists CLIENTS
(
    id_client varchar(36) not null,
    nom       varchar(50) not null,
    prenom    varchar(50),
    email     varchar(50) unique,
    adresse   varchar(200),
    telephone char(10) unique,
    unique (nom, prenom),
    primary key (id_client)
);
create table LIVRES
(
    ISBN        char(10)            not null primary key,
    titre       varchar(250)        not null,
    auteur      varchar(250)        not null,
    editeur     varchar(100)        not null,
    langue      varchar(5)          not null,
    nbrepages   integer             null,
    description text                null,
    annee       date,
    note        double default null null,
    prix        double
);
create unique index LIVRES_ISBN_uindex on LIVRES (ISBN);
create index search_auteur on LIVRES (auteur);
create index search_editeur on LIVRES (editeur);
create index search_titre on LIVRES (titre);
CREATE TABLE STOCK
(
    ISBN     char(10) unique,
    quantity int,
    primary key (isbn)
);
CREATE TABLE IF NOT EXISTS COMPTE
(
    identifiant varchar(20) unique,
    motDePasse  varchar(256),
    primary key (identifiant)
);
create table if not exists ASSOCIER
(
    identifiant char(50),
    id_client   char(36),
    unique (identifiant, id_client),
    foreign key (identifiant) references compte (identifiant) on delete cascade on update cascade,
    foreign key (id_client) references clients (id_client) on delete cascade on update cascade
);
CREATE TABLE IF NOT EXISTS PROMOTIONS
(
    id_promotion integer auto_increment not NULL,
    remise       integer,
    date_debut   datetime               not null,
    date_fin     datetime               not null,
    PRIMARY KEY (id_promotion)
);
CREATE TABLE IF NOT EXISTS APPLIQUER
(
    id_promotion integer,
    ISBN         char(10) unique,
    prix_remise  double,
    unique (id_promotion, ISBN),
    FOREIGN KEY (id_promotion) REFERENCES Promotions (id_promotion) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (ISBN) REFERENCES LIVRES (ISBN) ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS FACTURER
(
    id_client  char(36),
    ISBN       char(10),
    id_facture char(36) not null,
    #date_achat datetime not null,
    quantite   integer,
    PRIMARY KEY (id_facture, id_client, ISBN),
    FOREIGN KEY (ISBN) REFERENCES Livres (ISBN) ON DELETE NO ACTION ON UPDATE CASCADE,
    FOREIGN KEY (id_client) REFERENCES Clients (id_client) ON UPDATE CASCADE ON DELETE NO ACTION
);
CREATE TABLE IF NOT EXISTS EVALUER
(
    id_client   char(36),
    ISBN        char(10),
    note        integer NOT NULL,
    commentaire TEXT,
    date        datetime,
    primary key (id_client, ISBN),
    foreign key (ISBN) REFERENCES LIVRES (ISBN) ON DELETE CASCADE ON UPDATE CASCADE,
    foreign key (id_client) REFERENCES Clients (id_client) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE PANIER
(
    id_client char(36),
    ISBN      char(10),
    quantity  INTEGER,
    PRIMARY KEY (id_client, ISBN),
    FOREIGN KEY (id_client) REFERENCES Clients (id_client) ON DELETE NO ACTION ON UPDATE CASCADE,
    FOREIGN KEY (ISBN) references LIVRES (ISBN) ON DELETE NO ACTION ON UPDATE CASCADE
);
delimiter / /
create trigger update_book_note
    after
        insert
    on EVALUER
    for each row
BEGIN
    declare nbre_eval int;
    declare eval int;
    select sum(E.note)
    into eval
    from evaluer E
    where E.ISBN = new.ISBN;
    select count(E.isbn)
    into nbre_eval
    from EVALUER E
    where E.ISBN = NEW.ISBN;
    update
        livres
    set note = eval
    /
    nbre_eval
    where
  LIVRES.ISBN = NEW.ISBN;
end / / delimiter;
DELIMITER / /
CREATE PROCEDURE validate_uuid(IN in_uuid char(36))
    DETERMINISTIC NO SQL
BEGIN
    IF NOT (
        SELECT in_uuid REGEXP '[[:alnum:]]{8,}-[[:alnum:]]{4,}-[[:alnum:]]{4,}-[[:alnum:]]{4,}-[[:alnum:]]{12,}'
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET
                MESSAGE_TEXT = 'ID provided is not valid UUID format';
    END IF;
END / / DELIMITER;
DELIMITER / /
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
END / / DELIMITER;
DELIMITER / /
CREATE TRIGGER validate_client_id
    BEFORE
        INSERT
    ON Clients
    FOR EACH ROW
BEGIN
    CALL validate_uuid(NEW.id_client);
END / / DELIMITER;
DELIMITER / /
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
END / / DELIMITER;
DELIMITER / /
CREATE TRIGGER check_evaluation_per_user
    BEFORE
        INSERT
    ON Evaluer
    FOR EACH ROW
BEGIN
    IF (
           SELECT COUNT(*)
           FROM Evaluer
           WHERE id_client = NEW.id_client
             and isbn = NEW.isbn
       ) > 1 THEN
        SIGNAL SQLSTATE '45000'
            SET
                MESSAGE_TEXT = 'Product already evaluated';
    END IF;
END / / DELIMITER;
DELIMITER / /
CREATE TRIGGER validate_facture_id
    BEFORE
        INSERT
    ON Facturer
    FOR EACH ROW
BEGIN
    CALL validate_uuid(NEW.id_facture);
END / / DELIMITER;
DELIMITER / /
CREATE TRIGGER validate_client_email
    BEFORE
        INSERT
    ON Clients
    FOR EACH ROW
BEGIN
    CALL validate_email(New.email);
END / / DELIMITER;
DELIMITER / /
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
end / / DELIMITER;
delimiter / /
create procedure add_panier(id char(36), p_isbn char(10), quantite int)
begin
    declare nombre int;
    declare quantity_in_cart int;
    declare quantity_in_stock int;
    select count(id_client)
    into nombre
    from panier
    where id_client = id
      and PANIER.ISBN = p_isbn;
    if nombre > 0 then
        select quantity
        into quantity_in_cart
        from panier
        where id_client = id
          and PANIER.ISBN = p_isbn;
        select quantity
        into quantity_in_stock
        from stock
        where STOCK.ISBN = p_isbn;
        if (quantity_in_cart + quantite < 0) then
            signal sqlstate '45000'
                set
                    message_text = 'Vous etes entrain de retirer plus qu\'il y\'en a';
        elseif (quantity_in_stock - quantite < 0) then
            signal sqlstate '45000'
                set
                    message_text = 'La quantité est insuffisante en stock';
        end if;
        update
            panier
        set quantity = quantity_in_cart + quantite
        where id_client = id
          and PANIER.ISBN = p_isbn;
        update
            STOCK
        set quantity = quantity_in_stock - quantite
        where STOCK.ISBN = p_isbn;
    else
        insert into panier
        values (id, p_isbn, quantite);
    end if;
end / / delimiter;
delimiter / /
create trigger verify_quantite_on_insert
    before
        insert
    on panier
    for each row
begin
    declare quantity_in_stock int;
    select quantity
    into quantity_in_stock
    from STOCK
    where STOCK.ISBN = NEW.ISBN;
    if (NEW.quantity <= 0) then
        signal sqlstate '45000'
            set
                message_text = 'On ne peut pas inserer une quantité nulle ou negative';
    end if;
    if (quantity_in_stock < NEW.quantity) then
        signal sqlstate '45000'
            set
                message_text = 'La quantité est insuffisante en stock';
    end if;
    update
        STOCK
    set quantity = quantity_in_stock - NEW.quantity
    where STOCK.ISBN = NEW.ISBN;
end / / delimiter;
delimiter / /
create trigger set_prix_remise
    before
        insert
    on appliquer
    for each row
begin
    declare p_promo integer;
    declare p_prix_initial double;
    select prix
    into p_prix_initial
    from livres
    where LIVRES.ISBN = NEW.ISBN;
    select remise
    into p_promo
    from promotions P
    where P.id_promotion = NEW.id_promotion;
    set
        NEW.prix_remise = ((100 - p_promo) * p_prix_initial)
    /
    100;
end / / delimiter;
delimiter / /
create trigger update_prix_remise
    after
        update
    on PROMOTIONS
    for each row
begin
    declare p_promo integer;
    declare p_prix_initial double;
    if NEW.remise != OLD.remise then
        update
            appliquer A
        set A.prix_remise = A.prix_remise * (100 - NEW.remise)
        /
            (100 - OLD.remise)
            where
  A.id_promotion = NEW.id_promotion;
    end if;
end / / delimiter;
delimiter / /
create function get_prix_remise(p_isbn char(10)) returns double
    deterministic no sql
Begin
    declare p_prix double;
    declare compte int;
    select count(A.ISBN)
    into compte
    from APPLIQUER A
    where A.ISBN = p_isbn;
    if compte > 0 then
        select prix_remise
        into p_prix
        from appliquer A
        where A.ISBN = p_isbn;
        return p_prix;
    else
        select L.prix
        into p_prix
        from livres L
        where L.ISBN = p_isbn;
        return p_prix;
    end if;
end / / delimiter;
create table if not exists Commandes
(
    id_client  char(36) not null,
    id_facture char(36) not null,
    date       datetime not null,
    prixTotal  double   not null,
    primary key (id_client, id_facture)
);
delimiter / /
create procedure transfert_from_cart_to_bill(in p_idClient char(36))
    deterministic no sql
begin
    declare taxe_rate double;
    declare shipping int;
    declare date_facture datetime;
    declare new_id char(36);
    declare p_isbn char(10);
    declare p_prix double;
    declare p_quantity int;
    declare prix_t double;
    declare lecture_complete integer DEFAULT false;
    declare curseur cursor for
        select P.isbn,
               P.quantity
        from PANIER P
        where P.id_client = p_idClient;
    declare continue handler for not found
        set
            lecture_complete = TRUE;
    select current_timestamp
    into date_facture;
    select uuid()
    into new_id;
    set
        taxe_rate = 1.15;
    set
        shipping = 15;
    select sum(get_prix_remise(P.isbn) * P.quantity) * taxe_rate + shipping
    into prix_t
    from PANIER P
    where P.id_client = p_idClient;
    open curseur;
    lecteur:
    loop
        fetch curseur into p_isbn,
            p_quantity;
        if lecture_complete then
            leave lecteur;
        end if;
        insert into facturer
        values (p_idClient, p_isbn, new_id, p_quantity);
    end loop lecteur;
    insert into Commandes
    values (p_idClient, new_id, date_facture, prix_t);
    close curseur;
end / / delimiter;
delimiter / /
create trigger delete_books
    after
        insert
    on Commandes
    for each row
begin
    delete
    from panier P
    where P.id_client = NEW.id_client;
end / / delimiter;




