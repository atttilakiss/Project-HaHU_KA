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
        self.catalog_processing = bool()
        self.catalog_validation = bool()
        self.catalog_url = str()
        self.catalog_raw_lines = list()
        self.catalog_query = list()
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
        
        self.catalog_attributes_list_modified = [
                                'Kategória',
                                'start_production',
                                'end_production',  # special regex treatment needed
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
                                'Városi fogyasztás',  # floater regex treatment needed
                                'Országúti fogyasztás',  # floater regex treatment needed
                                'Vegyes fogyasztás',  # floater regex treatment needed
                                'Végsebesség',
                                'Gyorsulás',  # floater regex treatment needed
                                'Maximális forgatónyomaték',
                                'Maximális teljesítmény',  # special regex treatment needed
                                 ]


    def catalog_raw_download(self, catalog_url, catalog_validation):
        """
        downloading the catalog page via the url that had been found in the advertisement
        very raw format
        return is the full HTML page of the catalog
        """

        self.catalog_validation = catalog_validation

        if self.catalog_validation:
            if catalog_url != "no catalog":
                catalog_file_handler = urllib.request.urlopen(catalog_url)
                for line in catalog_file_handler:
                    self.catalog_raw_lines.append(line.decode().strip())  #0130_debug / still writing the catalog_raw_lines
                self.catalog_processing = True
                print('gathering data from the catalog: ', catalog_url)
            else:
                print("catalog_raw_download: no catalog url had been found")  #probably not going to work here
                self.catalog_processing = False


    def catalog_data_retrive(self, cur, catalog_url):
        """
        gathering the relevant catalog data from the raw HTML5 data
        """
        if self.catalog_validation:
            #creating the default_catalog_attribute dictionary
            for attribute in self.catalog_attributes_list:
                self.raw_catalog_attribute[attribute] = 'na'

            if self.catalog_processing:
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
                    elif k == 'Gyártási időszak' and v == 'na':
                        self.catalog_attributes['start_production'] = v
                        self.catalog_attributes['end_production'] = v
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

                    self.catalog_processing = True

            else:
                print("catalog_regex_processing: no catalog url had been found")  #probably not going to work here
                for attribute in self.catalog_attributes_list_modified:
                    self.catalog_attributes[attribute] = 'na'          
                #self.catalog_attributes = self.raw_catalog_attribute
                self.catalog_processing = False
        
        else:
            catalog_url_query_input = list()
            catalog_url_query_input.append(catalog_url)
            cur.execute("""SELECT * FROM Catalogs WHERE catalog_url= ?""", catalog_url_query_input)
            catalog_query_raw = cur.fetchall()
            for i in catalog_query_raw[0]:
                self.catalog_query.append(str(i))
        


