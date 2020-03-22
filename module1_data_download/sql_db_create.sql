--droping the tables
drop table if exists Advertisement;

drop table if exists Catalog;

--creating the table, Advertisement
create table if not EXISTS Advertisements (
	hirkod integer UNIQUE,
	region TEXT,
	adprice integer,
	numpictures integer,
	sellertype text,
	adoldness integer,
	postalcode integer,
	agegroup integer,
	km integer,
	clime integer,
	gas integer,
	shifter text,
	person_capacity integer,
	doorsnumber integer,
	documentvalid integer,
	color integer,
	brand text,
	model text,
	motor integer,
	eloresorolas integer,
	upload_date integer,
	description text,
	advertisement_url TEXT,
	catalog_url TEXT
	sales_date INTEGER,
	status text,
	download_date VARCHAR,
	sales_update_date VARCHAR);


--creating the table, Catalogs
create table if not EXISTS Catalogs (
	catalog_url TEXT UNIQUE,
	kategória TEXT,
	start_production TEXT,
	end_production TEXT,
	újkori_ára TEXT,
	kivitel TEXT,
	ajtók_száma TEXT,
	személyek TEXT,
	saját_tömeg TEXT,
	üzemanyagtank TEXT,
	csomagtér TEXT,
	üzemanyag TEXT,
	környezetvédelmi TEXT,
	hengerelrendezés TEXT,
	hengerek INT,
	hajtás TEXT,
	hengerűrtartalom TEXT,
	városi TEXT,
	országúti TEXT,
	vegyes TEXT,
	végsebesség TEXT,
	gyorsulás TEXT,
	nyomaték TEXT,
	teljesítmény TEXT);


--creating the table, Full Data
create table if not EXISTS Full_Data (
	hirkod integer UNIQUE,
	region TEXT,
	adprice integer,
	numpictures integer,
	sellertype text,
	adoldness integer,
	postalcode integer,
	agegroup integer,
	km integer,
	clime integer,
	gas integer,
	shifter text,
	person_capacity integer,
	doorsnumber integer,
	documentvalid integer,
	color integer,
	brand text,
	model text,
	motor integer,
	eloresorolas integer,
	upload_date integer,
	description text,
	advertisement_url TEXT,
	catalog_url TEXT,
	kategória TEXT,
	start_production TEXT,
	end_production TEXT,
	újkori_ára TEXT,
	kivitel TEXT,
	ajtók_száma TEXT,
	személyek TEXT,
	saját_tömeg TEXT,
	üzemanyagtank TEXT,
	csomagtér TEXT,
	üzemanyag TEXT,
	környezetvédelmi TEXT,
	hengerelrendezés TEXT,
	hengerek INT,
	hajtás TEXT,
	hengerűrtartalom TEXT,
	városi TEXT,
	országúti TEXT,
	vegyes TEXT,
	végsebesség TEXT,
	gyorsulás TEXT,
	nyomaték TEXT,
	teljesítmény TEXT);


--selecting all the data on the joint statement (catalog_id = catalog_id)
	select * from Advertisements Join Catalogs ON Advertisements.catalog_id = Catalogs.catalog_id


CREATE TABLE
IF NOT EXISTS Log_Data
(
	run_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	start_time VARCHAR,
	end_time VARCHAR,
	run_time VARCHAR,
	downloaded_advertisements VARCHAR,
	updated_advertisements VARCHAR,
	first_result_site_index VARCHAR,
	total_result_sites VARCHAR);