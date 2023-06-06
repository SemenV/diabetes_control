
DO $$ BEGIN 
UPDATE all_nagruzka SET nagruzka = 'test', nagr_type = 'subspline' WHERE useid = 1 and nagruzka_name = 'hod'; 
IF NOT FOUND THEN 
INSERT INTO all_nagruzka (useid, nagruzka_name, nagruzka, nagr_type) VALUES (1 , 'hod' , 'test2','linear'); 
END IF; 
END; 
$$