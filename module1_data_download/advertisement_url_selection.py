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
import time as time_

# developed modules
from advertisement_collect_class import *
from catalog_collect_class import *
from ad_data_catalog_data_compile import *
from json_file_saving_class import *
from SQL_load_class import *

class AdvertisementUrlSelection:
    def __init__(self):
        self.entry_site_url = 'https://www.hasznaltauto.hu/szemelyauto'
        self.result_site_index = list()
        self.entry_site_raw_lines = list()
        self.data_page_indexes = list()
        self.top_resultsite_index = str()
        self.raw_result_site_url = str()
        self.result_sites_to_parse = list()
        self.advertisement_urls_list = list()
        self.advert_site_number_prompt = int()
        self.first_result_site = str()
        self.start_time = str()
    
    def result_site_index_parsing(self):
        file_handler = urllib.request.urlopen(self.entry_site_url)
        for line in file_handler:
            self.entry_site_raw_lines.append(line.decode().strip())
        
        for raw_line in self.entry_site_raw_lines:
            if 'data-page' in raw_line:
                self.data_page_indexes.append(int(re.findall('" data-page="([0-9]+)', raw_line)[0]))

        self.top_resultsite_index = max(self.data_page_indexes)

        for raw_line in self.entry_site_raw_lines:
            if 'data-page' and 'talalatilista' in raw_line:
                result_site_url = re.findall('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+', raw_line)[0]
                if 'page' in result_site_url:
                    self.raw_result_site_url = result_site_url[:-1]
                    break

    def result_sites_list_compiling(self):
        """
        unused method, enhanced is in charge
        """
        if 1 == 2:
            first_result_site_prompt = int(input('first result site?: '))
            if first_result_site_prompt == 0:
                first_result_site_prompt == 1
            result_site_number_prompt = int(input('how many result sites?: '))

            for i in range(first_result_site_prompt, first_result_site_prompt + result_site_number_prompt+1):
                self.result_sites_to_parse.append(self.raw_result_site_url + str(i))
        
        #enhanced method on 2020_03_14/KA
        elif 1==1:
            #random start number of the result site
            self.first_result_site = random.randint(1, int(self.top_resultsite_index))  #determines the first result site index for parsing
            self.advert_site_number_prompt = int(input('how many advert sites?: '))
            self.start_time = time_.time()




    
    def result_site_parsing(self,result_site_url):
        result_site_raw_lines = list()
        file_handler = urllib.request.urlopen(result_site_url)
        for line in file_handler:
            result_site_raw_lines.append(line.decode().strip())
        
        for line in result_site_raw_lines:
            if '/szemelyauto/' in line and '/talalatilista/' not in line:
                try:
                    self.advertisement_urls_list.append(re.findall('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+', line)[0])
                except: continue

