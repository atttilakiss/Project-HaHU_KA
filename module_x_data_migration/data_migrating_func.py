import sqlalchemy as db
from sqlalchemy import exc
import psycopg2
import pandas as pd

import sqlite3
import numpy as np
import time

#run = int(input("run the script?"))
run = 0

postgres_path = 'postgresql://attilakiss:postgres1@localhost/hahu_project_database'
sqlite_path = '/Users/attilakiss/Desktop/project_HaHU_KA/Project-HaHU_KA/DB/test_db.db'

def populate_categorical_dictionaries(postgres_path):
    """
    - connecting to the postgresDB 
    - reads all the data from the categorical data tables that had been populated (e.g. brand, region) before
    - stores the query output in dictionaries, keys= 'advertisements','catalogs'
        - each key contains the corresponding tables (e.g. advertisements = (region, clime, gas, brand, model))
    - in the old database the categorical column names were inconsistent (hungarian and english names were both representing themselves) 
        - the (correct) table names had to be replaced in order to match the naming of the old database columns
    - the function returns two dictionaries:
        - df_dict = contains pandas dataframes of all the categorical tables (e.g. {'region': region_dataframe (region_id,region_name)})
        - df_dict_cat_col_names = contains dictionaries for oldDB column names and df_dict dataframes
    """


    #SQLalchemy connection
    engine = db.create_engine(postgres_path)
    connection = engine.connect()

    #variables
    df_dict = dict()
    df_dict_cat_col_names = dict()
    tables = ["region", "brand", "model", "category", "car_type", "environmental", "drive"]
    messed_up_names = {
        "category": "kategória",
        "car_type": "kivitel",
        "environmental": "környezetvédelmi",
        "drive": "hajtás"}

    #SQL query
    for table in tables:
        df_dict[table] = df = pd.read_sql("SELECT * FROM {0};".format(table), connection)
        df_dict_cat_col_names[table] = {str(table)+'_id':str(table)+'_name'} 

    #replacing column names
    for correct_name, messed_name in messed_up_names.items():
        
        df_dict[messed_name] = df_dict[correct_name]
        df_dict.pop(correct_name)

        df_dict_cat_col_names[messed_name] = df_dict_cat_col_names[correct_name]
        df_dict_cat_col_names.pop(correct_name)
        
    connection.close()
    return df_dict, df_dict_cat_col_names
    print('done - populate_categorical_dictionaries()')

if 1 == run:
    df_dict_cat, df_dict_cat_col_names = populate_categorical_dictionaries(postgres_path)


def read_old_db_tables(sqlite_path):
    """
    - connecting to the old database
    - querying from the oldDB, saves data into a dictionay, keys= 'advertisements', 'catalogs'
        - parsing the dates according to previously determined date formats
    - the function returns two dictionaries:
        - df_dict_old_tables: query results saved in df, with keys= 'advertisements', 'catalogs'
        - column_names: oldDB column names saved in lists, with keys= 'advertisements', 'catalogs'
    """

    #connecting to the old DB
    sql3_database = sqlite_path
    conn_sqlite3 = sqlite3.connect(sql3_database)
    
    #variables
    tables = ["advertisements","catalogs"]
    column_names = dict()
    df_dict_old_tables = dict()

    #date formats
    date_format_advertisements = '%Y%m%d'
    date_format_catalogs = '%Y' 

    #SQL query
    for table in tables:
        df_dict_old_tables[table] = df = pd.read_sql("SELECT * FROM {0}".format(table), 
        conn_sqlite3,
        parse_dates={
            'agegroup':date_format_advertisements, 
            'documentvalid': date_format_advertisements,
            'upload_date': date_format_advertisements,
            'sales_date': date_format_advertisements,
            'download_date': date_format_advertisements,
            'sales_update_date': date_format_advertisements,
            'start_production': date_format_catalogs,
            'end_production': date_format_catalogs,
            }
        )
        column_names[table] = df_dict_old_tables[table].columns.tolist()
    conn_sqlite3.close()
    return df_dict_old_tables, column_names
    print('done - read_old_db_tables()')


def read_new_db_tables(postgres_path):
    """
    - connecting to the new DB (Postgres)
    - querying from the new DB
    - the function returns a dictionary:
        - column_names = contains all the columns names from the new DB as a list, with keys= 'advertisements', 'catalogs'
    """
    #reads the new DB tables into pandas df

    #SQLalchemy connection
    engine = db.create_engine(postgres_path)
    connection = engine.connect()

    df_dict = dict()
    column_names = dict()
    tables = ["advertisements", "catalogs"]
    for table in tables:
        df_dict[table] = df = pd.read_sql("SELECT * FROM {0};".format(table), connection)
        column_names[table] = df_dict[table].columns.tolist()
    connection.close()
    return column_names
    print('done - read_new_db_tables()')

if 1 == run:
    #querying the the old DB (data, column names); querying the new DB (data, column names)
    new_column_names = read_new_db_tables(postgres_path)
    df_dict_old_tables, old_column_names = read_old_db_tables(sqlite_path)


    #creating the value pairs dicts for the renaming
    column_mapping = dict()
    column_mapping['advertisements'] = dict(zip(old_column_names['advertisements'], new_column_names['advertisements']))
    column_mapping['catalogs'] = dict(zip(old_column_names['catalogs'], new_column_names['catalogs']))


def categorical_data_mapping(df_dict_old_tables, df_dict_cat_col_names, df_dict_cat):
    """
    - creating a dictionary that contains a copy of the dataframe that holds the query result of the read_old_db_tables function
        - keys= 'advertisements','catalogs' / stored in new_db_tables
    - merging the categorical tables in one step, many actions are taking place at once:
        - iteration through the categorical columns (e.g. 'region', 'brand' etc.)
            - for every relevant column in advertisements or catalogs table, 
            the categorical data keys are replacing the old values 
            (e.g. 'region' column old value = 'Heves megye', new value = 0, 
            which is now serving a foreign key in the DB that points the 'Heves megye' value in the categorical table)
            - Pandas's merge method had been utilizied with an inner join method, the IDs are now stored in the same column name as in the new DB
            - old column dropped from the dataframe
    - reason of data loss: some values were missing from the categorical tables; the merging were using an inner join, so those rows that containing a missing value were left out altogether
    - the function returns a dictionary, that contains the modified old database with the keys= 'advertisements', 'catalogs'
    """

    #variables (output variable determination)
    new_db_tables = dict()

    #creating a copy of the DFs that contains the oldDB data, no modification is made
    for key in df_dict_old_tables.keys():
        new_db_tables[key] = df_dict_old_tables[key].copy()


    #merging the oldDB table with the categorical tables, saved in new DF
    for key in df_dict_cat_col_names.keys():
        if key in list(new_db_tables['advertisements'].columns.tolist()):
            new_db_tables['advertisements'] = new_db_tables['advertisements'].merge(
                df_dict_cat[key],
                left_on = key,
                right_on=list(df_dict_cat_col_names[key].values())[0]
            ).drop(columns=[key, list(df_dict_cat_col_names[key].values())[0]])
        elif key in list(new_db_tables['catalogs'].columns.tolist()):
            new_db_tables['catalogs'] = new_db_tables['catalogs'].merge(
                df_dict_cat[key],
                left_on=key,
                right_on=list(df_dict_cat_col_names[key].values())[0]
            ).drop(columns=[key, list(df_dict_cat_col_names[key].values())[0]])
    
    
    #increasing the key values of 'clime' by 1
    #otherwise their key value would have been 0, which cause a key error due to primary key constraints (NOTNULL) in SQL DBs
    new_db_tables['advertisements']['clime'] = new_db_tables['advertisements']['clime'] + 1
    
    #remapping the 'gas' column with their key values
    new_db_tables['advertisements']['gas'] = new_db_tables['advertisements']['gas'].replace(to_replace={
        0: 1,
        1: 2,
        2: 3,
        3: 5,
        5: 6,
        6: 7,
        7: 8,
        8: 9,
        9: 11,
        11: 12,
        12: 15,
        15: 16}, inplace = True)

    return new_db_tables
    print('done - categorical_data_mapping()')

if 1 == run:
    new_db_tables = categorical_data_mapping(df_dict_old_tables, df_dict_cat_col_names, df_dict_cat)



def boolean_data_mapping(new_db_tables):
    #change certain data to boolens in ADVERTISEMENTS (advertisements: "proseller", "highlighted", "is_sold")
    """
    - replacing values in three columns of the advertisements table with boolean values
        - columns = "proseller", "highlighted", "is_sold"
    - the function returns a dictionary, with the keys= 'advertisements', 'catalogs'
    """
    new_db_tables['advertisements'] = new_db_tables['advertisements'].replace(to_replace={
        'priv':0,
        'pro':1,
        'OPEN':0,
        'SOLD':1},
        inplace = False).astype({
            'sellertype':'bool',
            'eloresorolas':'bool',
            'status':'bool'
        })
    return new_db_tables
    print('done - boolean_data_mapping()')

if 1 == run:
    new_db_tables = boolean_data_mapping(new_db_tables)


def float_data_correction(new_db_tables):
    """
    - replacing the commas to dots in the catalogs table in the floater type columns
    - the function returns a dictionary, with the keys= 'advertisements', 'catalogs'
    """
    #replacing comma values to dots in CATALOGS
    false_data = ['városi', 'országúti', 'vegyes', 'gyorsulás']
    for column in false_data:
        new_db_tables['catalogs'][column] = new_db_tables['catalogs'][column].apply(lambda x: x.replace(',', '.'))

    return new_db_tables
    print('done - float_data_correction()')


if 1 == run:
    new_db_tables = float_data_correction(new_db_tables)


#determining the appropirate missing data according to the dtype
messed_data = dict()
messed_data['advertisements'] = {'region_id':['integer','null']}
messed_data['catalogs'] = {
    'category_id': ['integer', 'na'],
    'start_production': ['date','na'],
    'end_production': ['date','na'],
    'újkori_ára': ['numeric','na'],
    'car_type_id': ['integer', 'na'],
    'ajtók_száma': ['numeric','na'],
    'saját_tömeg': ['numeric', 'na'],
    'személyek': ['numeric', 'na'],
    'üzemanyagtank': ['numeric','na'],
    'csomagtér': ['numeric', 'na'],
    'environmental_id': ['integer', 'na'],
    'hengerelrendezés': ['text','na'],
    'hengerek': ['numeric', 'na'],
    'drive_id': ['integer', 'na'],
    'hengerűrtartalom': ['numeric', 'na'],
    'városi': ['numeric', 'na'],
    'országúti': ['numeric', 'na'],
    'vegyes': ['numeric', 'na'],
    'végsebesség': ['numeric', 'na'],
    'gyorsulás': ['numeric', 'na'],
    'nyomaték': ['numeric', 'na'],
    'teljesítmény': ['numeric', 'na']
    }


def missing_data_correction(messed_data, new_db_tables):
    """
    - replacing the missing data accoring to the dtype of the column
    - incorrect missing data values had been determined in a dict()
    - the function replacing the incorrect missing data (typically 'na') with a correct missing data format according to the dtype (in the SQL DB) of the column
    - the function returns a dictionary, with the keys= 'advertisements', 'catalogs' 
    """
    for key in messed_data.keys():
        for k, v in messed_data[key].items():
            if v[0] == 'numeric':
                new_db_tables[key][k].replace(v[1:], np.nan, inplace=True)
                new_db_tables[key][k].replace(r'^\s*$', np.nan, regex=True, inplace = True)
            elif v[0] == 'integer':
                new_db_tables[key][k].replace(v[1:], np.nan, inplace=True)
            elif v[0] == 'date':
                new_db_tables[key][k].replace(v[1:], 'NaT', inplace=True)
            elif v[0] == 'text':
                new_db_tables[key][k].replace(v[1:], 'NA', inplace=True)

    return new_db_tables
    print('done - missing_data_correction()')

if 1 == run:
    new_db_tables = missing_data_correction(messed_data, new_db_tables)

def column_renaming(new_db_tables, column_mapping):
    """
    - the function remapping the old column names (Sqlite) with new column names from the Postgres DB
    """
    #renaming the old DB with the new column names
    db_tables_renamed_formated = dict()
    db_tables_renamed_formated['advertisements'] = new_db_tables['advertisements'].copy().rename(columns=column_mapping['advertisements']).set_index('ad_id')
    db_tables_renamed_formated['catalogs'] = new_db_tables['catalogs'].copy().rename(columns=column_mapping['catalogs']).set_index('catalog_url')

    return db_tables_renamed_formated
    print('done - column_renaming()')

if 1 == run:
    db_tables_renamed_formated = column_renaming(new_db_tables, column_mapping)

#setting the proper datatypes for the columns
catalog_datatypes = list()
catalog_datatypes = (
   	{'category_id': 'Int64'},
   	{'start_production':'datetime64'},
   	{'end_production':'datetime64'},
   	{'msrp':'Int64'},
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
advertisement_datatypes= (
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


def dtype_setting(catalog_datatypes, advertisement_datatypes, db_tables_renamed_formated):
    """
    - the function transforms the column to numeric datatype in case of floater or integer datatypes
    - if the column is not a numeric type the scripts select the appropriate dtype and sets it for the column
    - the function returns a dictionary, with the keys= 'advertisements', 'catalogs'  
    """
    #transformation of the data dtypes in the dataframe
    for item in catalog_datatypes:
        for column, dtype in item.items():
            if dtype in ['Int64', 'float64']:
                db_tables_renamed_formated['catalogs'][column] = pd.to_numeric(db_tables_renamed_formated['catalogs'][column])
            else:
                db_tables_renamed_formated['catalogs'][column] = db_tables_renamed_formated['catalogs'][column].astype(dtype)

    for item in advertisement_datatypes:
        for column, dtype in item.items():
            if dtype in ['Int64', 'float64']:
                db_tables_renamed_formated['advertisements'][column] = pd.to_numeric(db_tables_renamed_formated['advertisements'][column])
            else:
                db_tables_renamed_formated['advertisements'][column] = db_tables_renamed_formated['advertisements'][column].astype(dtype)

    return db_tables_renamed_formated

if 1 == run:
    db_tables_renamed_formated = dtype_setting(catalog_datatypes, advertisement_datatypes, db_tables_renamed_formated)

"""
#checkpoint / all transformation done, next step is exporting into Postgres
print(db_tables_renamed_formated['catalogs'].info())
print(db_tables_renamed_formated['advertisements'].info())
"""

def df_to_sql(postgres_path, migration_object, db_tables_renamed_formated):
    """
    - the function validates an input parameter regarding to the object of the migration (if values == 3, catalogs and advertisements will be migrated also)
    - the function selects the migration object from the input paramteres
    - the function trying to export the data into the SQL database
        - if fails it is collecting the failed rows alongside with the error code
        - the failure log is saved in a csv file with the objectname and timestamp of the migration
    """
    #setting up the DB connection
    engine = db.create_engine(postgres_path)
    connection = engine.connect()
    
    #determining the error log variables
    catalog_errors = pd.DataFrame()
    catalog_error_types = pd.DataFrame(columns=['catalog_url','error_type', 'pgerror'])
    advertisements_errors = pd.DataFrame()
    advertisements_error_types = pd.DataFrame(columns = ['ad_id','error_type', 'pgerror'])

    #loading the DB into the Postgres SQL DB
    if migration_object == 1:
        for i in range(len(db_tables_renamed_formated['catalogs'])):
            try:
                db_tables_renamed_formated['catalogs'].iloc[i:i+1].to_sql(
                    name = 'catalogs', 
                    if_exists='append', 
                    con=connection)
            except exc.DBAPIError as ex:
                catalog_errors = catalog_errors.append(db_tables_renamed_formated['catalogs'].iloc[i:i+1])
                catalog_error_types = catalog_error_types.append({
                    'catalog_url': db_tables_renamed_formated['catalogs'].iloc[i:i+1].index[0],
                    'error_type': type(ex),
                    'pgerror': ex.orig.pgerror},
                    ignore_index=True)                
                continue
        
        catalog_error_types = catalog_error_types.set_index('catalog_url')
        catalog_errors = catalog_errors.merge(
            right = catalog_error_types,
            how='outer',
            left_index=True,
            right_index=True)
        mig_time = time.strftime("%Y%m%d_%H%M%S")
        catalog_errors.to_csv('catalog_errors_{0}.csv'.format(mig_time))

    elif migration_object == 2:
        for i in range(len(db_tables_renamed_formated['advertisements'])):
            try:
                db_tables_renamed_formated['advertisements'].iloc[i:i+1].to_sql(
                    name='advertisements',
                    if_exists='append',
                    con=connection)
            except exc.DBAPIError as ex:
                advertisements_errors = advertisements_errors.append(db_tables_renamed_formated['advertisements'].iloc[i:i+1])
                advertisements_error_types = advertisements_error_types.append(
                    {'ad_id': db_tables_renamed_formated['advertisements'].iloc[i:i+1].index[0],
                     'error_type': type(ex),
                     'pgerror': ex.orig.pgerror},
                    ignore_index=True)
                continue

        advertisements_error_types = advertisements_error_types.set_index('ad_id')
        advertisements_errors = advertisements_errors.merge(
            right=advertisements_error_types,
            how='outer',
            left_index = True,
            right_index = True)
        
        mig_time = time.strftime("%Y%m%d_%H%M%S")
        advertisements_errors.to_csv('advertisements_errors_{0}.csv'.format(mig_time))
    
    elif migration_object == 3:
        print('Method = both')
        #CATALOGS
        for i in range(len(db_tables_renamed_formated['catalogs'])):
            try:
                db_tables_renamed_formated['catalogs'].iloc[i:i+1].to_sql(
                    name='catalogs',
                    if_exists='append',
                    con=connection)
            except exc.DBAPIError as ex:
                catalog_errors = catalog_errors.append(db_tables_renamed_formated['catalogs'].iloc[i:i+1])
                catalog_error_types = catalog_error_types.append({
                    'catalog_url': db_tables_renamed_formated['catalogs'].iloc[i:i+1].index[0],
                    'error_type': type(ex),
                    'pgerror': ex.orig.pgerror},
                    ignore_index=True)                
                continue

        catalog_error_types = catalog_error_types.set_index('catalog_url')
        catalog_errors = catalog_errors.merge(
            right=catalog_error_types,
            how='outer',
            left_index=True,
            right_index=True)
        mig_time = time.strftime("%Y%m%d_%H%M%S")
        catalog_errors.to_csv('catalog_errors_{0}.csv'.format(mig_time))

        #ADVERTISEMENTS
        for i in range(len(db_tables_renamed_formated['advertisements'])):
            try:
                db_tables_renamed_formated['advertisements'].iloc[i:i+1].to_sql(
                    name='advertisements',
                    if_exists='append',
                    con=connection)
            except exc.DBAPIError as ex:
                advertisements_errors = advertisements_errors.append(db_tables_renamed_formated['advertisements'].iloc[i:i+1])
                advertisements_error_types = advertisements_error_types.append(
                    {'ad_id': db_tables_renamed_formated['advertisements'].iloc[i:i+1].index[0],
                     'error_type': type(ex),
                     'pgerror': ex.orig.pgerror},
                    ignore_index=True)
                continue

        advertisements_error_types = advertisements_error_types.set_index(
            'ad_id')
        advertisements_errors = advertisements_errors.merge(
            right=advertisements_error_types,
            how='outer',
            left_index=True,
            right_index=True)

        mig_time = time.strftime("%Y%m%d_%H%M%S")
        advertisements_errors.to_csv(
            'advertisements_errors_{0}.csv'.format(mig_time))
    
    
    connection.close()
if 1 == run:
    df_to_sql(migration_object, db_tables_renamed_formated)
