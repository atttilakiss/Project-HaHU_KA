#__init__ config might missing,
# so the parent module was not able to found,
# many exceptions had been raised,
# absolute and realtive import did not work neither,
# so this solution was the only one that actually worked
import sys
import sqlalchemy as db
import pandas as pd
import psycopg2
import sqlite3
import numpy as np
sys.path.append('/Users/attilakiss/Desktop/project_HaHU_KA/Project-HaHU_KA/module1_data_download')
import catalog_collect_class
import SQL_load_class
import URL_validation_class


#creating the list of the missing catalogURLs
missing_catalog_df = pd.DataFrame()
missing_catalog_df = pd.read_excel(
    '/Users/attilakiss/Desktop/project_HaHU_KA/Project-HaHU_KA/ad_id.xlsx',
    'missing_catalogs',
    header = None)

sql_database = '/Users/attilakiss/Desktop/project_HaHU_KA/Project-HaHU_KA/DB/test_db.db'
conn = sqlite3.connect(sql_database)
cur = conn.cursor()

missing_catalogs = missing_catalog_df.iloc[:,0].to_list()  #creating a list from the df
#catalog_validation = True  #manual input for the function / otherwise it would be evaluated
url_validation = URL_validation_class.URL_Validation()
for catalog in missing_catalogs:
    #validating the missing URL
    url_validation.catalog_url_validation(catalog, cur)

    #gathering the catalog data
    car_catalog = catalog_collect_class.CatalogDownload()
    # downloading the raw catalog data
    car_catalog.catalog_raw_download(catalog, url_validation.catalog_validation)
    car_catalog.catalog_data_retrive(cur, catalog) 

    #compiling the catalog data
    car_catalog.catalog_attributes['catalog_url'] = catalog

    #loading the cleaned catalog data into the SQL DB
    sql_load = SQL_load_class.SQL_load()
    sql_load.sql_load_catalog(car_catalog.catalog_attributes,
                              cur, 
                              url_validation.catalog_validation)
    conn.commit()

