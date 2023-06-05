DO $$ BEGIN
    CREATE TYPE ch_role_enum AS ENUM ('user', 'admin');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;



CREATE TABLE IF NOT EXISTS people
(
    idd  SERIAL PRIMARY KEY,
    login VARCHAR(100) UNIQUE, 
    passwordd VARCHAR(100),
	id_alice VARCHAR(1024) UNIQUE,
	ch_role ch_role_enum,
	stage INTEGER
);


CREATE TABLE IF NOT EXISTS all_nagruzka ( 
	ida SERIAL PRIMARY KEY,
	useid INTEGER,
	nagruzka_name VARCHAR(2048), 	
	nagruzka VARCHAR(2048),
	UNIQUE (useid, nagruzka_name)
);

CREATE TABLE IF NOT EXISTS eda ( 
	ide SERIAL PRIMARY KEY,
	useid INTEGER,
	ch_day timestamp UNIQUE, 
	menu_eda VARCHAR(2048),  
	ch_nagruzka VARCHAR(2048),
	time_nagruzka VARCHAR(200),
	FOREIGN KEY (useid) REFERENCES people (idd)
);	

CREATE TABLE IF NOT EXISTS eda_tmp ( 
	ide SERIAL PRIMARY KEY,
	id_alice VARCHAR(1024) UNIQUE, 
	current_food VARCHAR(4000),  
	FOREIGN KEY (id_alice) REFERENCES people (id_alice)
);

CREATE TABLE IF NOT EXISTS reg_tmp ( 
	ide SERIAL PRIMARY KEY,
	id_alice VARCHAR(1024) UNIQUE, 
	login VARCHAR(100) UNIQUE, 
	passwordd VARCHAR(100),
	FOREIGN KEY (id_alice) REFERENCES people (id_alice)
);


	