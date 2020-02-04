#2020_01_28

# standard modules
import json
import urllib.request, urllib.parse, urllib.error
import sqlite3
import re
import sys
from datetime import *
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class CatalogDownload:
    def __init__(self):
        self.processing = bool()
        self.catalog_raw_lines = list()
        self.catalog_attributes_list = [
                                'Kategória',
                                'Gyártási időszak',  #special regex treatment needed
                                'Újkori ára',
                                'Kivitel',
                                'Ajtók száma',
                                'személyek',
                                'Saját tömeg',
                                'Üzemanyagtank',
                                'Csomagtér',
                                'Üzemanyag',
                                'Környezetvédelmi',
                                'Hengerelrendezés',
                                'Hengerek száma',
                                'Hajtás',
                                'Hengerűrtartalom',
                                'Városi fogyasztás',  #floater regex treatment needed
                                'Országúti fogyasztás',  #floater regex treatment needed
                                'Vegyes fogyasztás',  #floater regex treatment needed
                                'Végsebesség',
                                'Gyorsulás',  #floater regex treatment needed
                                'Maximális forgatónyomaték',
                                'Maximális teljesítmény',  #special regex treatment needed
                                ]
        self.raw_catalog_attribute = dict()
        self.default_catalog_attribute = dict()
        self.catalog_attributes = dict()
        self.catalog_integer_attributes = [
                                'Újkori ára',
                                'Ajtók száma',
                                'személyek',
                                'Saját tömeg',
                                'Üzemanyagtank',
                                'Csomagtér',
                                'Hengerek száma',
                                'Hengerűrtartalom',
                                'Végsebesség',
                                'Maximális forgatónyomaték',
                                ]
        self.catalog_floater_attributes = [
                                'Városi fogyasztás',
                                'Országúti fogyasztás',
                                'Vegyes fogyasztás',
                                'Gyorsulás',
                                ]


    def catalog_raw_download(self, catalog_url):
        """
        downloading the catalog page via the url that had been found in the advertisement
        very raw format
        return is the full HTML page of the catalog
        """
        if catalog_url:
            #0130_debug / manual entry
            #catalog_url = 'https://katalogus.hasznaltauto.hu/cadillac/escalade_6.0_v8_hybrid_platinum_automata-118336'
            #catalog_url = 'https://katalogus.hasznaltauto.hu/volvo/xc60_2.0_d4_momentum_awd-114650'

            catalog_file_handler = urllib.request.urlopen(catalog_url)
            for line in catalog_file_handler:
                self.catalog_raw_lines.append(line.decode().strip())  #0130_debug / still writing the catalog_raw_lines
            self.processing = True
        else:
            print("no catalog url had been found")  #probably not going to work here
            self.processing = False


    def catalog_data_retrive(self):
        """
        gathering the relevant catalog data from the raw HTML5 data
        """
        if self.processing:
        #creating the default_catalog_attribute dictionary
            for attribute in self.catalog_attributes_list:
                self.raw_catalog_attribute[attribute] = 'na'

            for attribute in self.catalog_attributes_list:
                for line in self.catalog_raw_lines:
                    if re.search(attribute, line):
                        self.raw_catalog_attribute[attribute] = self.catalog_raw_lines[self.catalog_raw_lines.index(line)+1]


            for k,v in self.raw_catalog_attribute.items():
                if v == 'na':
                    continue
                else:
                    try:
                        self.raw_catalog_attribute[k] = re.findall('>(\w.+)<', v)[0]
                    except:
                        self.raw_catalog_attribute[k] = re.findall('>(\w)<', v)[0]

            for k,v in self.raw_catalog_attribute.items():
                if v == 'na':
                    self.catalog_attributes[k] = v
                else:
                    if k in self.catalog_integer_attributes:
                        self.catalog_attributes[k] = re.findall('([0-9]*)', re.sub('\s', '',v))[0]
                    elif k in self.catalog_floater_attributes:
                        self.catalog_attributes[k] = re.findall('([0-9]*,[0-9]*)', re.sub('\s', '',v))[0]
                    elif k == 'Gyártási időszak':
                        self.catalog_attributes['start_production'] = re.findall('([0-9]*).', re.sub('\s', '',v))[0]
                        try:
                            self.catalog_attributes['end_production'] = re.findall('-([0-9]*)', re.sub('\s', '',v))[0]
                        except:
                            self.catalog_attributes['end_production'] = '9999'
                    elif k == 'Maximális teljesítmény':
                        self.catalog_attributes[k] = re.findall('([0-9]*)LE', re.sub('\s', '',v))[0]
                    else:
                        self.catalog_attributes[k] = v

                self.processing = True

        else:
            print("no catalog url had been found")  #probably not going to work here
            self.processing = False
