import json
import urllib.request, urllib.parse, urllib.error
import sqlite3
import re
import sys
from datetime import *
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from catalog_collect_class import *

class FullData:
    def __init__(self):
        self.full_data = dict()
        self.advertisement_data = dict()
        self.catalog_data = dict()

    def full_data_compile(self, ad_url, advertisement_data, description, catalog_url, catalog_data):
        """
        compiling the available data into one dictionary, and adds the URLs
        """
        #compiling advertisement_data
        for k, v in advertisement_data.items():
            self.advertisement_data[k] = v
        self.advertisement_data['description'] = description
        self.advertisement_data['ad_URL'] = ad_url
        self.advertisement_data['catalog_url'] = catalog_url

        #compiling catalog_data
        self.catalog_data['catalog_url'] = catalog_url
        for k, v in catalog_data.items():
            self.catalog_data[k] = v


        #compliling full_data
        for k, v in self.advertisement_data.items():
            self.full_data[k] = v
        for k, v in self.catalog_data.items():
            self.full_data[k] = v
