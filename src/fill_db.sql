TRUNCATE TABLE people CASCADE;
TRUNCATE TABLE all_nagruzka CASCADE ;
TRUNCATE TABLE eda CASCADE ;
TRUNCATE TABLE eda_tmp CASCADE ;
TRUNCATE TABLE reg_tmp CASCADE ;
TRUNCATE TABLE localfood CASCADE ;
TRUNCATE TABLE usereda CASCADE ;




INSERT  INTO people (login, passwordd,id_alice,ch_role) VALUES ('admin','admin', '3E18334CDD236883E268CE71B6CD2A884B13FE86A046015CCF39208CBA83C7D0','admin');
INSERT  INTO people (login, passwordd,id_alice,ch_role) VALUES ('семен','с', 'qwe','user');
INSERT  INTO people (login, passwordd,id_alice,ch_role) VALUES ('таня','т', 'asd','user');

INSERT  INTO localfood (prod_name, prod_param) VALUES ('абрикос',9);
INSERT  INTO localfood (prod_name, prod_param) VALUES ('вафли',62.5);
INSERT  INTO localfood (prod_name, prod_param) VALUES ('шоколад горький',48.2);
INSERT  INTO localfood (prod_name, prod_param) VALUES ('макароны отварные',20);
INSERT  INTO localfood (prod_name, prod_param) VALUES ('каша гречневая',14.6);
INSERT  INTO localfood (prod_name, prod_param) VALUES ('хлеб',45.1);
INSERT  INTO localfood (prod_name, prod_param) VALUES ('йогурт',3.5);
INSERT  INTO localfood (prod_name, prod_param) VALUES ('йогурт сладкий',8.5);
INSERT  INTO localfood (prod_name, prod_param) VALUES ('молоко',4.8);
INSERT  INTO localfood (prod_name, prod_param) VALUES ('творог',3);


INSERT  INTO usereda (useid, prod_name, prod_param) VALUES(
(SELECT idd FROM public.people where login = 'admin'),
'теремок блин с грибами',
18.2
);

INSERT  INTO usereda (useid, prod_name, prod_param) VALUES(
(SELECT idd FROM public.people where login = 'admin'),
'теремок блин золотая рыбка',
19
);

INSERT  INTO usereda (useid, prod_name, prod_param) VALUES(
(SELECT idd FROM public.people where login = 'admin'),
'теремок медовик',
44.8
);

INSERT  INTO usereda (useid, prod_name, prod_param) VALUES(
(SELECT idd FROM public.people where login = 'admin'),
'теремок салат оливье',
6.7
);

INSERT  INTO all_nagruzka (useid, nagruzka_name, nagruzka, nagr_type) VALUES(
(SELECT idd FROM public.people where login = 'admin'),
'прогулка',
'2.2',
'linear'
);

INSERT  INTO all_nagruzka (useid, nagruzka_name, nagruzka, nagr_type) VALUES(
(SELECT idd FROM public.people where login = 'admin'),
'велосипед',
'2.7',
'linear'
);

INSERT  INTO all_nagruzka (useid, nagruzka_name, nagruzka, nagr_type) VALUES(
(SELECT idd FROM public.people where login = 'admin'),
'прогулка сад',
'[0.0, 0.0, 0.0, 1.0, 2.2, 0.0, 2.0, 6.5, 0.0]',
'subspline'
);


INSERT  INTO all_nagruzka (useid, nagruzka_name, nagruzka, nagr_type) VALUES(
(SELECT idd FROM public.people where login = 'admin'),
'плавание танцы',
'[0.0, 0.0, 0.0, 1.0, 6.0, 5.0, 2.0, 8.5, 0.0]',
'subspline'
);

