drop database if exists projet_glo_2005;
create database projet_glo_2005;
use projet_glo_2005;
create table if not exists CLIENTS (
  id_client varchar(36) not null,
  nom varchar(50) not null,
  prenom varchar(50),
  email varchar(50) unique,
  adresse varchar(200),
  telephone char(11) unique,
  unique (nom, prenom),
  primary key (id_client)
);
CREATE TABLE IF NOT EXISTS LIVRES (
  ISBN BIGINT,
  titre varchar(250) NOT NULL,
  langue varchar(5) NOT NULL,
  nbrepages integer,
  note double default 0.0,
  quantity integer,
  description text,
  primary key (ISBN)
);
create fulltext index search_titre on livres(titre);
CREATE TABLE IF NOT EXISTS EDITEURS (
  id_editeur int auto_increment,
  nom varchar(100) unique,
  primary key (id_editeur)
);
CREATE TABLE IF NOT EXISTS PUBLIER (
  ISBN BIGINT,
  id_editeur integer not null,
  annee date,
  PRIMARY KEY (ISBN, id_editeur),
  foreign key (ISBN) references livres (ISBN) on delete cascade on update cascade,
  foreign key (id_editeur) references EDITEURS (id_editeur) on delete cascade on update cascade
);
CREATE TABLE IF NOT EXISTS AUTEURS (
  id_auteur int auto_increment,
  nom varchar(250) not null,
  primary key (id_auteur)
);
create table if not exists ECRIRE (
  ISBN BIGINT,
  id_auteur integer not null,
  unique (ISBN, id_auteur),
  FOREIGN KEY (ISBN) REFERENCES LIVRES (ISBN) on delete cascade on update cascade,
  foreign key (id_auteur) REFERENCES AUTEURS (ID_AUTEUR) ON delete cascade on update cascade
);
CREATE TABLE IF NOT EXISTS COMPTE (
  identifiant varchar(20),
  motDePasse varchar(50),
  primary key (identifiant)
);
create table if not exists ASSOCIER (
  identifiant char(50),
  id_client char(36),
  unique (identifiant, id_client),
  foreign key (identifiant) references compte (identifiant) on delete cascade on update cascade,
  foreign key (id_client) references clients (id_client) on delete cascade on update cascade
);
CREATE TABLE IF NOT EXISTS PROMOTIONS (
  id_promotion integer unique not NULL,
  remise integer,
  date_debut datetime not null,
  date_fin datetime not null,
  PRIMARY KEY (id_promotion)
);
CREATE TABLE IF NOT EXISTS APPLIQUER (
  id_promotion integer,
  ISBN BIGINT,
  prix_remise double,
  unique (id_promotion, ISBN),
  FOREIGN KEY (id_promotion) REFERENCES Promotions (id_promotion) ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (ISBN) REFERENCES LIVRES (ISBN) ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS FACTURER (
  id_client char(36),
  ISBN BIGINT,
  id_facture char(36) not null,
  date_achat datetime not null,
  quantite integer,
  PRIMARY KEY (id_facture),
  FOREIGN KEY (ISBN) REFERENCES Livres (ISBN) ON DELETE NO ACTION ON UPDATE CASCADE,
  FOREIGN KEY (id_client) REFERENCES Clients (id_client) ON UPDATE CASCADE ON DELETE NO ACTION
);
CREATE TABLE IF NOT EXISTS EVALUER (
  id_client char(36),
  ISBN BIGINT,
  note integer NOT NULL,
  commentaire TEXT,
  date datetime,
  primary key (id_client, ISBN),
  foreign key (ISBN) REFERENCES LIVRES (ISBN) ON DELETE CASCADE ON UPDATE CASCADE,
  foreign key (id_client) REFERENCES Clients (id_client) ON DELETE CASCADE ON UPDATE CASCADE
);
CREATE TABLE PANIER (
  id_client char(36),
  ISBN BIGINT,
  quantity INTEGER,
  PRIMARY KEY (id_client, ISBN),
  FOREIGN KEY (id_client) REFERENCES Clients (id_client) ON DELETE NO ACTION ON UPDATE CASCADE,
  FOREIGN KEY (ISBN) references LIVRES (ISBN) ON DELETE NO ACTION ON UPDATE CASCADE
);
delimiter / / create procedure insert_tuple_ecrire(isbn bigint, nom_auteur varchar(250))
deterministic no sql begin declare id integer;
select
  id_auteur into id
from
  auteurs
where
  nom = nom_auteur;
insert into
  ecrire (isbn, id_auteur)
VALUES
  (ISBN, id);
end / / delimiter;
delimiter / / create procedure insert_tuple_publier(
  isbn bigint,
  nom_editeur varchar(100),
  publisher_date date
) deterministic no sql begin declare id integer;
select
  id_editeur into id
from
  editeurs
where
  nom = nom_editeur;
insert into
  PUBLIER (isbn, id_editeur, annee)
VALUES
  (ISBN, id, publisher_date);
end / / delimiter;
DELIMITER / / CREATE PROCEDURE validate_uuid(IN in_uuid char(36))
DETERMINISTIC NO SQL BEGIN IF NOT (
  SELECT
    in_uuid REGEXP '[[:alnum:]]{8,}-[[:alnum:]]{4,}-[[:alnum:]]{4,}-[[:alnum:]]{4,}-[[:alnum:]]{12,}'
) THEN SIGNAL SQLSTATE '45000'
SET
  MESSAGE_TEXT = 'ID provided is not valid UUID format';
END IF;
END / / DELIMITER ;
DELIMITER / / CREATE PROCEDURE validate_email(IN in_email varchar(100)) DETERMINISTIC NO SQL BEGIN IF NOT (
  SELECT
    in_email REGEXP '^[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$'
) THEN SIGNAL SQLSTATE '45000'
SET
  MESSAGE_TEXT = 'E-mail address provided is not valild e-mail format';
END IF;
END / / DELIMITER;
DELIMITER / / CREATE TRIGGER validate_client_id BEFORE
INSERT
  ON Clients FOR EACH ROW BEGIN CALL validate_uuid(NEW.id_client);
END / / DELIMITER;
DELIMITER / / CREATE TRIGGER valider_note_evaluer BEFORE
INSERT
  ON Evaluer FOR EACH ROW BEGIN IF NEW.note < 0
  or NEW.note > 5 THEN SIGNAL SQLSTATE '45000'
SET
  MESSAGE_TEXT = 'rate between 0 and 5';
END IF;
END / / DELIMITER;
DELIMITER / / CREATE TRIGGER check_evaluation_per_user BEFORE

INSERT
  ON Evaluer FOR EACH ROW BEGIN IF (
    SELECT
      COUNT(*)
    FROM
      Evaluer
    WHERE
      id_client = NEW.id_client
  ) > 1 THEN SIGNAL SQLSTATE '45000'
SET
  MESSAGE_TEXT = 'Product already evaluated';
END IF;
END / / DELIMITER ;
DELIMITER / / CREATE TRIGGER validate_facture_id BEFORE
INSERT
  ON Facturer FOR EACH ROW BEGIN CALL validate_uuid(NEW.id_facture);
END / / DELIMITER ;
DELIMITER / / CREATE TRIGGER validate_promotion_id BEFORE
INSERT
  ON Promotions FOR EACH ROW BEGIN CALL validate_uuid(NEW.id_promotion);
END / / DELIMITER ;
DELIMITER / / CREATE TRIGGER validate_client_email BEFORE
INSERT
  ON Clients FOR EACH ROW BEGIN CALL validate_email(New.email);
END / / DELIMITER ;
DELIMITER / / CREATE TRIGGER valider_insertion_tuple_promotion BEFORE
INSERT
  ON promotions FOR EACH ROW begin IF NEW.date_debut > NEW.date_fin then signal sqlstate '45000'
set
  message_text = 'La date de debut ne peut pas etre superieur à la date de fin ';
end if;
IF NEW.remise > 100 THEN signal sqlstate '45000'
set
  message_text = 'La remise ne peut pas exceder 100% ';
end if;
IF CURRENT_DATE > NEW.date_debut then signal sqlstate '45000'
set
  message_text = 'La date de debut ne peut pas pas être inférieure à la date courrante';
end if;
end / / DELIMITER ;

delimiter / /
create procedure add_panier (IN id char(36), In isbn bigint, In quantite int)
begin
declare nombre int;
declare quantity_in_stock int;
select
  count(*) into nombre
from
  panier
where
  id_client = id
  and ISBN = isbn;
if nombre > 0 then
select
  quantity into quantity_in_stock
from
  panier
where
  id_client = id
  and ISBN = isbn;
update
  panier
set
  quantity = quantity_in_stock + quantite
where
  id_client = id
  and ISBN = isbn;
  else
insert into
  panier
values
  (id, isbn, quantite);
end if;
end / / delimiter ;
delimiter / / create trigger verify_quantite_on_insert before
insert
  on panier for each row begin declare quantity_in_stock int;
select
  quantity into quantity_in_stock
from
  LIVRES
where
  LIVRES.ISBN = NEW.ISBN;
if (quantity_in_stock < NEW.quantity) then signal sqlstate '45000'
set
  message_text = 'La quantité est insuffisante';
end if;
end / / delimiter ;
delimiter / / create trigger update_stock_livres_on_insert
after
insert
  on panier for each row begin declare quantity_in_stock int;
select
  quantity into quantity_in_stock
from
  LIVRES
where
  LIVRES.ISBN = NEW.ISBN;
update
  livres
set
  quantity = quantity_in_stock - NEW.quantity
where
  ISBN = NEW.ISBN;
end / / delimiter ;
delimiter / / create trigger verify_quantite_on_update before
update
  on panier for each row begin declare quantity_in_stock int;
select
  quantity into quantity_in_stock
from
  LIVRES
where
  LIVRES.ISBN = NEW.ISBN;
if (quantity_in_stock < NEW.quantity) then signal sqlstate '45000'
set
  message_text = 'La quantité est insuffisante';
end if;
end / / delimiter ;
delimiter / / create trigger update_stock_livres_on_update
after
update
  on panier for each row begin declare quantity_in_stock int;
select
  quantity into quantity_in_stock
from
  LIVRES
where
  LIVRES.ISBN = NEW.ISBN;
update
  livres
set
  quantity = quantity_in_stock - NEW.quantity
where
  ISBN = NEW.ISBN;
end //
delimiter ;

call add_panier('dcfdf3e7-ba0f-11ec-83df-706655b22fd0', 8987059752, 1);
call add_panier('dcfdf3e7-ba0f-11ec-83df-706655b22fd0', 645241001173, 1);
select * from panier;

delete from panier where quantity > 0;