DELIMITER //
u
CREATE TRIGGER validate_client_id
    BEFORE INSERT
    ON Clients
    FOR EACH ROW
BEGIN
    CALL validate_uuid(NEW.id_client);
END//
DELIMITER ;