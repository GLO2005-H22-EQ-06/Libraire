create table if not exists Clients (
    idClient char(36) not null ,
    nom varchar(20) not null ,
    prenom varchar(20),
    email varchar(20),
    adresse varchar(50),
    telephone char(11),
    PRIMARY KEY (idClient)
);
