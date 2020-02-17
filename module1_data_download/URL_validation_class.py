# standard modules
import json
import urllib.request
import urllib.parse
import urllib.error
import sqlite3
import re
import sys
from datetime import *
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class URL_Validation:
    def __init__(self):
        self.advert_url_list = list()
        self.catalog_url_list = list()
        self.validated_advert_urls = list()
        self.catalog_validation = bool()

    def advertisement_url_validation(self, advertisement_urls_list, cur):
        cur.execute("""SELECT advertisement_url FROM URLs""")
        URL_query = cur.fetchall()
        for url in URL_query:
            self.advert_url_list.append(str(url[0]))

        for i in advertisement_urls_list:
            if i in self.advert_url_list:
                print('data related to the url already in the DB: ', i)
            else:
                self.validated_advert_urls.append(i)
    
    def catalog_url_validation(self, catalog_url, cur):
        cur.execute("""SELECT catalog_url FROM URLs""")
        catalog_url_query = cur.fetchall()
        for url in catalog_url_query:
            self.catalog_url_list.append(str(url[0]))

        if catalog_url in self.catalog_url_list:
            self.catalog_validation = False
        else:
            self.catalog_validation = True