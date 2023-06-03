SELECT idd
	FROM people WHERE login = 'таня' AND passwordd = 'т';
	
	
SELECT ch_day, menu_eda,ch_nagruzka,time_nagruzka
	FROM eda WHERE useid = 1 and ch_day > '2023-06-03 00:00:00+03' 
	AND ch_day <  '2023-06-03 23:59:59+03';