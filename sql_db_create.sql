--droping the tables
drop table if exists Advertisement;

drop table if exists Catalog;

--creating the table, Advertisement
create table if not EXISTS Advertisements (
	region TEXT,
	hirkod integer UNIQUE,
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
	doorsnumber integer,
	documentvalid integer,
	color integer,
	brand text,
	model text,
	motor integer,
	eloresorolas integer,
	description text,
	upload_date integer,
	size_n integer,
	catalog_id TEXT);


--creating the table, Catalogs
create table if not EXISTS Catalogs (
	catalog_id TEXT UNIQUE,
	kategória TEXT,
	gyártási_időszak TEXT,
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
	teljesítmény TEXT,
	gumiméret TEXT);

--selecting all the data on the joint statement (catalog_id = catalog_id)
	select * from Advertisements Join Catalogs ON Advertisements.catalog_id = Catalogs.catalog_id
