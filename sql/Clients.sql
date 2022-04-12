
select uuid();
insert into clients values (uuid(), "Toukam", 'Harold', "haroldtouks@gmail.com", "Bof", "4185715806");
call add_panier("1089bca7-ba77-11ec-8314-f430b9af64a8", "0001713191", -7);

select abs(-10.5);


select COUNT(*) from panier where id_client = "1089bca7-ba77-11ec-8314-f430b9af64a8" and ISBN = "000100039X";

select quantity from panier where id_client = "1089bca7-ba77-11ec-8314-f430b9af64a8" and ISBN = "000100039X";

select quantity into quantity_in_stock from stock where STOCK.ISBN = ISBN;