#2020_01_23

# standard modules
import json
import urllib.request, urllib.parse, urllib.error
import sqlite3
import re
import sys
from datetime import *
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class PageDownload:
    def __init__(self):
        self.page_url_link = str()
        self.raw_lines = list()
        self.output_filename_user_input = str()
        self.output_filename = str()
        self.url_valid = True
        self.processing = bool()

        self.line_keys = ['var utag_data', 'Leírás', 'katalogus']
        self.utag_data = list()
        self.advertisement_attributes = [
                'hirkod',
                'region',
                'ad_price',
                'num_pictures',
                'seller_type',
                'ad_oldness',
                'postal_code',
                'age_group',
                'km',
                'clime',
                'gas',
                'shifter',
                'size',
                'doors_number',
                'document_valid',
                'color',
                'brand',
                'model',
                'motor',
                'eloresorolas',
                ]
        self.processed_advertisement_data = dict()
        self.description = str()
        self.catalog_url = str()
        self.primary_data = dict()


    def URL_prompt(self):
        """
        prompt an URL for downloading
        """
        self.url_valid = False
        while self.url_valid == False:

            self.page_url_link = input("please paste the url: ")
            if len(self.page_url_link) == 0:
                break

            #self.page_url_link = 'https://www.hasznaltauto.hu/szemelyauto/mercedes-benz/ml-osztaly/mercedes-benz_ml-osztaly_ml_250_bluetec_automata_nem_legrugos_szervizelt_auto_valos_km-15357362'
            #self.page_url_link = 'https://google/'  #for testing only


            #enhancement: URL format testing with regex 2020_01_23 / done
            url_validation = URLValidator()
            try:
                url_validation(self.page_url_link)
                self.url_valid = True
                print("URL was ok")
            except ValidationError:
                self.url_valid = False
                print('URL was invalid')
        if self.page_url_link:
            self.processing = True


    def URL_raw_download(self):
        """
        downloading the page of the provided URL;
        very raw format
        return is a list with the full HTML page
        """
        if self.processing:
            file_handler = urllib.request.urlopen(self.page_url_link)
            for line in file_handler:
                self.raw_lines.append(line.decode().strip())
        else:
            print("no url for downloanding")
            self.processing = False

    def primary_data_retrieve(self):
        """
        gathering the utag data from the raw HTML5 data
        gathering the description from the raw HTML5 data
        gathering the catalog URL link from the raw HTML5 data
        """
        if self.processing:
            #primary data categories to be saved by the algorithm
            var_utag_data = True
            description_data = True
            cat_url = True

            #gathering the 'var utag_data'
            try:
                line_key = self.line_keys[0]
                for line in self.raw_lines:
                    if line_key in line:
                        self.utag_data = line.split(',')  #first returned value, utag_data in sliced format
                var_utag_data = True

            except:
                print("no 'var utag_data' had been found or analysis of utag_data failed")
                var_utag_data = False  #if no var utag_data found it stops running


            #Enhancement point: regex analysis of utag_data
            if var_utag_data:
                #enhanced method 0204
                #new parsing method
                utag_data_attributes_raw = list()
                for attribute in self.advertisement_attributes:
                    for line in self.utag_data:  #for all the attributes in the previously provided list, it looks for it in every line / less effective, more precise method
                        if re.search(attribute, line):
                            if 'event_name' in line or 'subject' in line:
                                continue
                            else:
                                utag_data_attributes_raw.append(line)  #if it finds it, it append to a raw data list

                #creating a blank advertisement data dictionary
                attributes_dict_raw = dict()
                for attribute in self.advertisement_attributes:
                    attributes_dict_raw[attribute] = 'na'

                for attribute in utag_data_attributes_raw:
                    #saves advertisement attributes data in dictionary, where the keys are the elements of the self.avertisement_attributes
                    attributes_dict_raw[self.advertisement_attributes[self.advertisement_attributes.index(re.findall('"(.+)":', attribute)[0])]] = re.findall(':(.+)', attribute)[0]


                #removing the remaining unnecessary charachters
                for key, value in attributes_dict_raw.items():
                    if '"' in value or '/' in value or key in ['age_group', 'document_valid']:  #if a special charachter left in the value
                        try:
                            processed_value = str()  #blank value for data self.processing
                            processed_value = re.sub('"', '', value)
                            self.processed_advertisement_data[key] = processed_value  #if it finds a special charachter it is self.processing and saving it into the same variable used before
                            processed_value = re.sub('/', '-', processed_value)
                            self.processed_advertisement_data[key] = processed_value  #next step of self.processing, if it is not possible continue to the next iteration of the loop
                            processed_value = re.sub('\\\\', '', processed_value)  # '\\\\' was the only way to find '\\' in the string
                            self.processed_advertisement_data[key] = processed_value
                        except:
                            continue

                    else:
                        self.processed_advertisement_data[key] = value  #this data is cleaned and formated


            #Enhancement point: calculating the precise date of advertisement upload
            today = date.today()
            raw_upload_date = (today + timedelta(-int(self.processed_advertisement_data['ad_oldness']))).strftime('%Y%m%d')
            self.processed_advertisement_data['upload_date'] = re.sub('[\W_]+', '', raw_upload_date)

            #Enhancement point: reformating the 'document_valid' and 'age_group' date formats
            #requesting the data and formating the data
            preformated_dates = dict()
            for k,v in self.processed_advertisement_data.items():
                if k == 'age_group':
                    try:
                        preformated_age_group = v.split('-')
                        if len(preformated_age_group[1]) == 1:
                            self.processed_advertisement_data['age_group'] = preformated_age_group[0] + '0' + preformated_age_group[1] + '01'
                        else:
                            self.processed_advertisement_data['age_group'] = preformated_age_group[0] + preformated_age_group[1] + '01'
                    except:
                        self.processed_advertisement_data['age_group'] = '19000101'
                elif k == 'document_valid':
                    try:
                        preformated_document_valid = v.split('-')
                        if len(preformated_document_valid[1]) == 1:
                            self.processed_advertisement_data['document_valid'] = preformated_document_valid[0] + '0' + preformated_document_valid[1] + '01'
                        else:
                            self.processed_advertisement_data['document_valid'] = preformated_document_valid[0] + preformated_document_valid[1] + '01'
                    except:
                        self.processed_advertisement_data['document_valid'] = '19000101'

            #gathering the 'description' of the advertisement
            if var_utag_data:
                try:
                    line_key = self.line_keys[1]
                    for line in self.raw_lines:
                        if line_key in line and len(line) <= 15:  #???
                            description_raw = self.raw_lines[self.raw_lines.index(line) + 1]  #saves the following line of the raw code, where the valuable data is stored
                            self.description = re.sub('<div>', '',re.sub('</div>', '', description_raw))  #removes the anchor tags from the raw data
                except:
                    print("no description had been found")
                    description_data = False


            #gathering the 'catalog' of the advertisement
            catalog_exclude1 = 'https://katalogus.hasznaltauto.hu/'
            #enhancement point 2: manufacturer and model data should be gathered and compiled for URL
            catalog_exclude2 = ('http://katalogus.hasznaltauto.hu/' + (self.processed_advertisement_data['brand']).lower() + '/' + (self.processed_advertisement_data['model']).lower()).replace(' ','_') #the manucaturer and the model should be added to the URL
            catalog_exclude_urls = [catalog_exclude1, catalog_exclude2]

            if var_utag_data:
                try:
                    line_key = self.line_keys[2]
                    catalog_url_list_raw = list()
                    for line in self.raw_lines:
                        if line_key in line:
                            catalog_url_list_raw.append(re.findall('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+',line))  #looking for an URL link, usually finds three

                    #moving to catalog_url_list_raw from the nested list type to a regular list
                    catalog_url_list = list()
                    for raw_list in catalog_url_list_raw:
                        catalog_url_list.append(raw_list[0])
                    
                    self.catalog_url = catalog_url_list[0]
                    for catalog_url_raw in catalog_url_list:
                        if len(self.catalog_url) > len(catalog_url_raw):
                            continue
                        else:
                            self.catalog_url = catalog_url_raw
                    
                    if self.catalog_url in catalog_exclude_urls:
                        cat_url = False
                    else:
                        cat_url = True
                        
                    """
                    for catalog_url in catalog_url_list:
                        if catalog_url in catalog_exclude_urls:
                            #print('excluding: ', catalog_url)
                            continue
                        else:
                            self.catalog_url = catalog_url
                            #print('keeping :' ,self.catalog_url)

                    if len(self.catalog_url) > 0:
                        cat_url = True
                    else:
                        cat_url = False
                    """
                except:
                    print("no relevant catalog url had been found")  #never gets here, because the catalog main site always in the advertisement site
                    cat_url = False


            #compiling the primary data into a dictionary
            if var_utag_data:
                self.primary_data['utag_data'] = self.processed_advertisement_data
            else:
                print("nothing to be saved")  #if no 'var utag_data' nothing will be saved related to the original URL

            if description_data:
                self.primary_data['description'] = self.description
            else:
                print("no description to be saved")
                self.primary_data['description'] = "no description"  #if no description, it will save "no description" as an explanation

            if cat_url:
                self.primary_data['catalog_url'] = self.catalog_url
            else:
                print("no catalog url to be saved")
                self.primary_data['catalog_url'] = "no catalog"  #if no relevant catalog data had been found "no catalog" will be saved as an explanation

        else:
            print("no url for downloading")
            self.processing = False
