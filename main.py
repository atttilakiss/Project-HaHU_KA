#2020_01_22

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
from url_collect_class import *
from catalog_collect_class import *


#gathering the advertisement page
car_page = PageDownload()  #creating an instance of the PageDownload class
car_page.URL_prompt()  #method that is asking for an URL;currently disabled 2020_01_23
car_page.URL_raw_download()  #downloading the page in raw HTML5 format
car_page.primary_data_retrieve()  #gathering the primary data from the downloaded raw HTML5 page
car_page.json_file_saving()  #asking the user about the saving possibility


#gathering the catalog page
car_catalog = CatalogDownload()
car_catalog.catalog_raw_download(car_page.primary_data['catalog_url'][0])
car_catalog.catalog_data_retrive()


advertisement_full_data = dict()
for k, v in car_page.processed_advertisement_data.items():
    advertisement_full_data[k] = v
for k, v in car_catalog.catalog_attributes.items():
    advertisement_full_data[k] = v

for k, v in advertisement_full_data.items():
    print('k: ', k, 'v: ', v)
