# standard modules
import json
import urllib.request, urllib.parse, urllib.error
import sqlite3
import re
import sys
from datetime import *
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

# developed modules
from advertisement_collect_class import *
from catalog_collect_class import *
from ad_data_catalog_data_compile import *
from json_file_saving_class import *


class SQL_load():
    def __init__(self):
        self.sql_database = '/Users/attilakiss/Desktop/project_HaHU_KA/Project-HaHU_KA/DB/test_db.db'
        self.load_data_list = list()

    def sql_load_advertisement(self, data_to_load_dictionary, cur):

        #assembling the load data list for advertisement data
        for k, v in data_to_load_dictionary.items():
            self.load_data_list.append(v)
        #sales status added 0210
        self.load_data_list.append('OPEN')  #status
        self.load_data_list.append(datetime.today().strftime('%Y%m%d'))  # download date
        self.load_data_list.append(datetime.today().strftime('%Y%m%d'))  # sales_update_date

        cur.execute("""INSERT OR IGNORE INTO Advertisements ('hirkod', 'region', 'adprice', 'numpictures', 'sellertype',
                        'adoldness', 'postalcode', 'agegroup', 'km', 'clime', 'gas', 'shifter','person_capacity', 'doorsnumber', 'documentvalid', 'color', 'brand',
                        'model', 'motor', 'eloresorolas', 'upload_date', 'description', 'advertisement_url', 'catalog_url', 'status', 'download_date', 'sales_update_date')
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", self.load_data_list)

        self.load_data_list = []
        print("Loading into the advert_DB: ", data_to_load_dictionary['ad_URL'])

    def sql_load_catalog(self, data_to_load_dictionary, cur, catalog_validation):
        if catalog_validation:
            #assembling the load data list for advertisement data
            for k, v in data_to_load_dictionary.items():
                self.load_data_list.append(v)

            cur.execute("""INSERT OR IGNORE INTO Catalogs ('catalog_url', 'kategória','start_production', 'end_production',
                            'újkori_ára', 'kivitel', 'ajtók_száma', 'személyek', 'saját_tömeg','üzemanyagtank',
                            'csomagtér', 'üzemanyag', 'környezetvédelmi', 'hengerelrendezés',
                            'hengerek', 'hajtás', 'hengerűrtartalom','városi','országúti', 'vegyes',
                            'végsebesség', 'gyorsulás','nyomaték', 'teljesítmény')
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", self.load_data_list)

            self.load_data_list = []

    def sql_load_full(self, data_to_load_dictionary, cur, catalog_validation, catalog_query, advertisement_data):
        if catalog_validation:
            #assembling the load data list for advertisement data
            for k, v in data_to_load_dictionary.items():
                self.load_data_list.append(v)

            cur.execute("""INSERT OR IGNORE INTO Full_Data ('hirkod', 'region', 'adprice', 'numpictures', 'sellertype',
                            'adoldness', 'postalcode', 'agegroup', 'km', 'clime', 'gas', 'shifter','person_capacity',
                            'doorsnumber', 'documentvalid', 'color', 'brand', 'model', 'motor', 'eloresorolas',
                            'upload_date', 'description', 'advertisement_url', 'catalog_url', 'kategória','start_production',
                            'end_production', 'újkori_ára', 'kivitel', 'ajtók_száma', 'személyek', 'saját_tömeg','üzemanyagtank',
                            'csomagtér', 'üzemanyag', 'környezetvédelmi', 'hengerelrendezés',
                            'hengerek', 'hajtás', 'hengerűrtartalom','városi','országúti', 'vegyes',
                            'végsebesség', 'gyorsulás','nyomaték', 'teljesítmény')
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
                                    ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", self.load_data_list)

        else:
            for k, v in advertisement_data.items():
                self.load_data_list.append(v)
            #self.load_data_list.extend(catalog_query[1:])
            for i in catalog_query[1:]:
               self.load_data_list.append(i)
            
            cur.execute("""INSERT OR IGNORE INTO Full_Data ('hirkod', 'region', 'adprice', 'numpictures', 'sellertype',
                        'adoldness', 'postalcode', 'agegroup', 'km', 'clime', 'gas', 'shifter','person_capacity',
                        'doorsnumber', 'documentvalid', 'color', 'brand', 'model', 'motor', 'eloresorolas',
                        'upload_date', 'description', 'advertisement_url', 'catalog_url', 'kategória','start_production',
                        'end_production', 'újkori_ára', 'kivitel', 'ajtók_száma', 'személyek', 'saját_tömeg','üzemanyagtank',
                        'csomagtér', 'üzemanyag', 'környezetvédelmi', 'hengerelrendezés',
                        'hengerek', 'hajtás', 'hengerűrtartalom','városi','országúti', 'vegyes',
                        'végsebesség', 'gyorsulás','nyomaték', 'teljesítmény')
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
                                ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", self.load_data_list)


        self.load_data_list = []


    def sql_load_url(self, url_list, cur):
        cur.execute("""INSERT OR IGNORE INTO URLs ('result_site_url', 'advertisement_url', 'catalog_url')
                        VALUES (?,?,?)""", url_list)
