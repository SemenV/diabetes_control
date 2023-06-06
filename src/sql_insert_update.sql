DO $$
BEGIN
UPDATE people SET login = 'aaaaaaa', passwordd = 'bbbbbbb' WHERE id_alice = 'xxx';
IF NOT FOUND THEN
 INSERT INTO people (login, passwordd,id_alice )values ('vvvvv','zzzzzz','xxx'); 	 
END IF;
END; 
$$