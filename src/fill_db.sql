TRUNCATE TABLE people CASCADE;
TRUNCATE TABLE all_nagruzka CASCADE ;
TRUNCATE TABLE eda CASCADE ;




INSERT  INTO people (login, passwordd,id_alice) VALUES ('таня','т', 'u432');
INSERT  INTO people (login, passwordd,id_alice) VALUES ('q','w', '1');
INSERT  INTO people (login, passwordd,id_alice) VALUES ('семен3','семен', 'qwerty');
INSERT  INTO people (id_alice) VALUES ('тест_только_алисы');
INSERT  INTO people (login, passwordd) VALUES ('тест_логина','фыв');


INSERT  INTO all_nagruzka (useid, nagruzka_name,nagruzka) VALUES (
(SELECT idd FROM people WHERE login = 'таня' AND passwordd = 'т'),
'hod',
'test_data'
);




INSERT  INTO eda (useid, ch_day, menu_eda) VALUES (
(SELECT idd FROM people where login = 'таня'),
'2023-06-02 10:10:10+03',
'макароны, творог'
);
INSERT  INTO eda (useid, ch_day, menu_eda) VALUES (
(SELECT idd FROM people where login = 'таня'),
'2023-06-02 16:10:10+03',
'сметана, огурцы'
);

INSERT  INTO eda (useid, ch_day, menu_eda,ch_nagruzka,time_nagruzka) VALUES (
(SELECT idd FROM people where id_alice = 'u432'),
'2023-06-03 14:14:14+03',
'греча',
'hod',
'5мин'
);

UPDATE people SET id_alice = 'alice123' WHERE login = 'таня' AND passwordd = 'т';
UPDATE people SET login = 'lkj', passwordd = 'lkj' WHERE id_alice = 'тест_только_алисы';







