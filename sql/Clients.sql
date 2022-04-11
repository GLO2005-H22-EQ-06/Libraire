drop table livres;
drop table clients;
drop table promotions;
drop table produits;
drop table editeurs;
drop table ordinateurs;



select count(*) from panier where id_produit = '5f1cbc91-af0d-11ec-acf3-645d863fa25e' and id_client ='ab2d0fc0-7224-11ec-8ef2-b658b885fb3e';
delete from produits where quantity > -400;
select distinct c3 from books;
drop table langues;
insert into langues (code_lang) values ("fr");
select distinct titre from livres;
select * from books;