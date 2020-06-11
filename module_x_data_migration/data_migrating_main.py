import sqlalchemy as db
import pandas as pd
import psycopg2
import sqlite3

import data_migrating_func as mig_func


postgres_path = 'postgresql://attilakiss:postgres1@localhost/hahu_project_database'
sqlite_path = '/Users/attilakiss/Desktop/project_HaHU_KA/Project-HaHU_KA/DB/test_db.db'

#determining the necessary VARIABLES

#used at missing_data_correction()
messed_missing_data = dict()
messed_missing_data['advertisements'] = {'region_id': ['integer', 'null']}
messed_missing_data['catalogs'] = {
    'category_id': ['integer', 'na'],
    'start_production': ['date', 'na'],
    'end_production': ['date', 'na'],
    'újkori_ára': ['numeric', 'na'],
    'car_type_id': ['integer', 'na'],
    'ajtók_száma': ['numeric', 'na'],
    'saját_tömeg': ['numeric', 'na'],
    'személyek': ['numeric', 'na'],
    'üzemanyagtank': ['numeric', 'na'],
    'csomagtér': ['numeric', 'na'],
    'environmental_id': ['integer', 'na'],
    'hengerelrendezés': ['text', 'na'],
    'hengerek': ['numeric', 'na'],
    'drive_id': ['integer', 'na'],
    'hengerűrtartalom': ['numeric', 'na'],
    'városi': ['numeric', 'na'],
    'országúti': ['numeric', 'na'],
    'vegyes': ['numeric', 'na'],
    'végsebesség': ['numeric', 'na'],
    'gyorsulás': ['numeric', 'na'],
    'nyomaték': ['numeric', 'na'],
    'teljesítmény': ['numeric', 'na']}




#setting the appropriate datatypes for the columns
catalog_datatypes = list()
catalog_datatypes = (
    {'category_id': 'Int64'},
   	{'start_production': 'datetime64'},
   	{'end_production': 'datetime64'},
   	{'msrp': 'Int64'},
   	{'car_type_id': 'Int64'},
   	{'doorsnumber': 'Int64'},
   	{'person_capacity': 'Int64'},
   	{'weight': 'Int64'},
   	{'fuel_tank': 'Int64'},
   	{'boot_capacity': 'Int64'},
   	{'fuel': 'object'},
   	{'environmental_id': 'Int64'},
   	{'cylinder_layout': 'object'},
   	{'cylinders': 'Int64'},
   	{'drive_id': 'Int64'},
   	{'ccm': 'Int64'},
   	{'consump_city': 'float64'},
   	{'consump_highway': 'float64'},
   	{'consump_mixed': 'float64'},
   	{'top_speed': 'Int64'},
   	{'acceleration': 'float64'},
   	{'torque': 'Int64'},
   	{'power': 'Int64'})

advertisement_datatypes = list()
advertisement_datatypes = (
    {'region_id': 'Int64'},
    {'ad_price': 'Int64'},
    {'numpictures': 'Int64'},
    {'proseller': 'bool'},
    {'adoldness': 'Int64'},
    {'postalcode': 'Int64'},
    {'production': 'datetime64'},
    {'mileage': 'Int64'},
    {'clime_id': 'Int64'},
    {'gas_id': 'Int64'},
    {'shifter': 'object'},
    {'person_capacity': 'Int64'},
    {'doorsnumber': 'Int64'},
    {'documentvalid': 'datetime64'},
    {'color': 'Int64'},
    {'brand_id': 'Int64'},
    {'model_id': 'Int64'},
    {'ccm': 'Int64'},
    {'highlighted': 'bool'},
    {'upload_date': 'datetime64'},
    {'description': 'object'},
    {'advertisement_url': 'object'},
    {'catalog_url': 'object'},
    {'sales_date': 'datetime64'},
    {'is_sold': 'bool'},
    {'download_date': 'datetime64'},
    {'sales_update_date': 'datetime64'})


#FUNCTIONS of the migration process

#querying the categorical data from the new SQL DB
dict_categorical_df, dict_categorical_col_names = mig_func.populate_categorical_dictionaries(postgres_path)


#querying all the data from the old SQL DB
dict_old_tables_df, old_column_names = mig_func.read_old_db_tables(sqlite_path)
print('old_db_query')
print(dict_old_tables_df['advertisements'].info())

#querying the DB column names from the new SQL DB
new_column_names = mig_func.read_new_db_tables(postgres_path)


#creating the value pairs dicts for the renaming
column_mapping = dict()
column_mapping['advertisements'] = dict(zip(
    old_column_names['advertisements'],
    new_column_names['advertisements']))
column_mapping['catalogs'] = dict(zip(
    old_column_names['catalogs'],
    new_column_names['catalogs']))


#data mapping / copying the data from the oldDB into the newDB dataframe
#former data loss issue point
new_db_tables = mig_func.categorical_data_mapping(dict_old_tables_df, dict_categorical_col_names, dict_categorical_df)


#replacing the values in the boolean relevant columns of the advertisements table
new_db_tables = mig_func.boolean_data_mapping(new_db_tables)


#correcting the floater values of the catalogs table (replacing comas with dots)
#caused a data error at postgres importing
new_db_tables = mig_func.float_data_correction(new_db_tables)


#replacing the missing values in the DF accoring to the dtype of the SQL Db
#caused a data error at postgres importing / 'na' and ' ' values were not recognisable in case of numeric or floater dtypes
new_db_tables = mig_func.missing_data_correction(messed_missing_data, new_db_tables)


#renaming the old DB with the new column names
db_tables_renamed_formated = mig_func.column_renaming(new_db_tables, column_mapping)



#setting the appropriate dtype for the DF columns, accoring to the SQL DB requirements
db_tables_renamed_formated = mig_func.dtype_setting(catalog_datatypes, advertisement_datatypes, db_tables_renamed_formated)


#masking the phone numbers possibly could be found in the description of the advertisement
db_tables_renamed_formated['advertisements']['description'] = db_tables_renamed_formated['advertisements']['description'].replace(
    r'[0-9]{4}','0000', regex = True, inplace = True)


#data transformation is done, next step is data exporting
#data migration to catalogs and advertisements tables
migration_object = input('what object should be migrated?\n1=catalogs\n2=advertisements\n3=both\ninput:')
mig_func.df_to_sql(postgres_path, int(migration_object),db_tables_renamed_formated)

print('migration done')
