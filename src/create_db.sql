CREATE TABLE IF NOT EXISTS people
(
    idd SERIAL PRIMARY KEY,
    login VARCHAR(100) UNIQUE, 
    passwordd VARCHAR(100),
	id_alice VARCHAR(1024) UNIQUE
);


CREATE TABLE IF NOT EXISTS all_nagruzka ( 
	ida SERIAL PRIMARY KEY,
	useid INTEGER ,
	nagruzka_name VARCHAR(2048) UNIQUE, 	
	nagruzka VARCHAR(2048),  
	FOREIGN KEY (useid) REFERENCES people (idd)
);

CREATE TABLE IF NOT EXISTS eda ( 
	ide SERIAL PRIMARY KEY,
	useid INTEGER,
	ch_day timestamp UNIQUE, 
	menu_eda VARCHAR(2048),  
	ch_nagruzka VARCHAR(2048),
	time_nagruzka VARCHAR(200),
	FOREIGN KEY (useid) REFERENCES people (idd),
	FOREIGN KEY (ch_nagruzka) REFERENCES all_nagruzka (nagruzka_name)
);	
	