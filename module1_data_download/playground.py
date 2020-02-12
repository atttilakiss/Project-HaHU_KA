

# standard modules
import json
import urllib.request, urllib.parse, urllib.error
import sqlite3
import re
import sys
from datetime import *


catalog_attributes_list = [
                        'Kategória',
                        'Gyártási időszak',  #special regex treatment needed
                        'Újkori ára',
                        'Kivitel',
                        'Ajtók száma',
                        'személyek',
                        'Saját tömeg',
                        '(Üzemanyagtank)',
                        'Csomagtér',
                        '(Üzemanyag)',
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


catalog_raw_lines = list()

catalog_url = 'https://katalogus.hasznaltauto.hu/cadillac/escalade_6.0_v8_hybrid_platinum_automata-118336'
catalog_url = 'https://katalogus.hasznaltauto.hu/volvo/xc60_2.0_d4_momentum_awd-114650'

catalog_file_handler = urllib.request.urlopen(catalog_url)
for line in catalog_file_handler:
    catalog_raw_lines.append(line.decode().strip())  #0130_debug / still writing the catalog_raw_lines
"""
catalog_attribute_counter = 0
for line in catalog_raw_lines:
    #print(line)
    #print(self.catalog_raw_lines.index(line))
    if catalog_attributes_list[catalog_attribute_counter] in line:
        print(catalog_attributes_list[catalog_attribute_counter])
        print(line)
        catalog_attribute_counter +=1
        if catalog_attribute_counter == len(catalog_attributes_list):  break
    elif catalog_attributes_list[catalog_attribute_counter] in line:
        catalog_attribute_counter +=1
        if catalog_attribute_counter == len(catalog_attributes_list):  break
"""
for line in catalog_raw_lines:
    if re.search('Felszereltség', line):
        print(line)
        felszereltség = line

undesired_attribute = catalog_raw_lines.index(felszereltség)+2
for attribute in catalog_attributes_list:
    for line in catalog_raw_lines:
        if re.search(attribute, line):
            if line == catalog_raw_lines[undesired_attribute]:
                continue
            else:
                print(attribute, " - ", line)
