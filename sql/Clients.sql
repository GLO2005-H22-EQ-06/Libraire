DELIMITER //

CREATE TRIGGER validate_client_id
    BEFORE INSERT
    ON Clients
    FOR EACH ROW
BEGIN
    CALL validate_uuid(NEW.id_client);
END//
DELIMITER ;

drop table livres;

alter table livres
se