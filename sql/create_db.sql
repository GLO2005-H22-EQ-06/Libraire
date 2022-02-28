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

CREATE TABLE Produits(
    id_produit char(36) not null, #le uuid de python retourne 36 caracteres donc j'ai mis à 36
    prix double,
    quantity integer,
    PRIMARY KEY (id_produit)
);

CREATE TABLE Promotions(
    id_promotion char(36) not NULL,
    remise integer,
    date_debut datetime not null,
    date_fin datetime not null,
    PRIMARY KEY (id_promotion)
);

CREATE TABLE Appliquer(
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

DROP TABLE Clients;
DROP TABLE Facturer