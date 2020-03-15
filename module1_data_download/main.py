#2020_01_22150

# standard modules
import json
import urllib.request, urllib.parse, urllib.error
import sqlite3
import re
import sys
from datetime import *
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import random

# developed modules
from advertisement_collect_class import *
from catalog_collect_class import *
from ad_data_catalog_data_compile import *
from json_file_saving_class import *
from SQL_load_class import *
from advertisement_url_selection import *
from URL_validation_class import *

#downloading the result sites and selecting the advertisement urls
result_site = AdvertisementUrlSelection()
result_site.result_site_index_parsing()
result_site.result_sites_list_compiling()
downloaded_advert_site = 0  # enhanced method on 2020_03_14/KA
res_site_url_index = result_site.first_result_site # enhanced method on 2020_03_14/KA

#enhanced method on 2020_03_14/KA
while downloaded_advert_site < result_site.advert_site_number_prompt:
    result_url = str(result_site.raw_result_site_url) + \
        str(res_site_url_index)  # recieving the first result site

    result_site.result_site_parsing(result_url)  #creates a list full of advertisement URLs

    sql_database = '/Users/attilakiss/Desktop/project_HaHU_KA/Project-HaHU_KA/DB/test_db.db'
    conn = sqlite3.connect(sql_database)
    cur = conn.cursor()
    print('gathering data from the result site: ', result_url, '\n')
    #advert url validation
    url_validation = URL_Validation()
    url_validation.advertisement_url_validation(result_site.advertisement_urls_list, cur)

    for advert_url in url_validation.validated_advert_urls:  #selects only one element from the list of advertisement urls
        if downloaded_advert_site < result_site.advert_site_number_prompt:

            #gathering the advertisement page
            car_page = PageDownload()  #creating an instance of the PageDownload class
            car_page.URL_prompt(advert_url)  #method that is asking for an URL;currently disabled 2020_01_23
            car_page.URL_raw_download()  #downloading the page in raw HTML5 format
            car_page.primary_data_retrieve()  #gathering the primary data from the downloaded raw HTML5 page

            #validating the catalog url
            url_validation.catalog_url_validation(car_page.primary_data['catalog_url'], cur)

            #gathering the catalog page
            car_catalog = CatalogDownload()  #creating an instance of the CatalogDownload class
            car_catalog.catalog_raw_download(car_page.primary_data['catalog_url'], url_validation.catalog_validation)  #downloading the catalog page that had been found in advertisement data
            # parsing the catalog page and saves data
            car_catalog.catalog_data_retrive(cur, car_page.primary_data['catalog_url'])


            #compiling the available data
            full_data = FullData()  #creating an instance for full data compiling
            full_data.full_data_compile(car_page.page_url_link, car_page.processed_advertisement_data, car_page.primary_data['description'], car_page.primary_data['catalog_url'], car_catalog.catalog_attributes)  #compiling the available data
            full_data.url_list_compile(result_url, car_page.page_url_link, car_page.primary_data['catalog_url'])


            #saving the gathered data into JSON
            if 1 == 2:
                json_file_saving = JSON_saving()  #creating an instance for json filesaving
                json_file_saving.json_saving(full_data.advertisement_data, full_data.catalog_data, full_data.full_data)  #the function prompts the user for the data to be saved


            #loading the retrieved data into the SQL database
            sql_database = '/Users/attilakiss/Desktop/project_HaHU_KA/Project-HaHU_KA/DB/test_db.db'
            conn = sqlite3.connect(sql_database)
            cur = conn.cursor()

            sql_load = SQL_load()
            sql_load.sql_load_advertisement(full_data.advertisement_data, cur)
            sql_load.sql_load_catalog(full_data.catalog_data, cur, url_validation.catalog_validation)
            #this SQL Table is not in use anymore
            #sql_load.sql_load_full(full_data.full_data, cur, url_validation.catalog_validation,
            #                       car_catalog.catalog_query, full_data.advertisement_data)
            sql_load.sql_load_url(full_data.url_data, cur)


            conn.commit()

            #enhanced method on 2020_03_14/KA
            downloaded_advert_site += 1
            print('downloaded advertisements: ', downloaded_advert_site)

            
        else:   pass
    res_site_url_index += 1
    if res_site_url_index > result_site.top_resultsite_index:  break  #breaks the while cycle if the res_site index is greater than the top index (it would cause an unreachable site error)



    conn.close()
