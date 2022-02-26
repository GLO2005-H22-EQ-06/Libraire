CREATE TABLE Produits(
    id_produit char(12) not null,
    prix double,
    quantity integer,
    PRIMARY KEY (id_produit)
);

CREATE TABLE Promotions(
    id_promotion char(12) not NULL,
    remise integer,
    date_debut datetime not null,
    date_fin datetime not null,
    PRIMARY KEY (id_promotion)
);

CREATE TABLE Appliquer(
    id_promotion char(12),
    id_produit char(12),
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