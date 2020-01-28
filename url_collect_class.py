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
                'region',
                'hirkod',
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
            """
            self.page_url_link = input("please paste the url: ")
            if len(self.page_url_link) == 0:
                break
            """
            self.page_url_link = 'https://www.hasznaltauto.hu/szemelyauto/cadillac/escalade/cadillac_escalade_6_0_v8_hybrid_platinum_automata_nezze_meg_a_videot_is-15189613'
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

    def json_file_saving(self):
        """
        saving the provided dataset in JSON format
        saved data can be selected
        exception handling had been impemented
        """
        if self.processing:
            saving = input("Do you wanna save results in JSON?")
            if len(saving) == 0:
                active = False
                data_determination_necessary = False
            else:
                active = True
                data_determination_necessary = True

            while data_determination_necessary:
                print("what data would you like to save?\n1 - raw_lines\n2 - primary_data\n3 - processed_advertisement_data")
                file_determination = input("Hit Enter for no saving; provide number: ")

                try:
                    if len(file_determination) == 0:
                        active = False
                        break
                    file_determination_formatted = int(file_determination)
                    if len(file_determination) == 0:
                        active = False
                        data_determination_necessary = False
                        break
                    elif file_determination_formatted == 1:
                        active = True
                        data_determination_necessary = False
                        saving_data = self.raw_lines
                        #print(saving_data[0])
                    elif file_determination_formatted == 2:
                        active = True
                        data_determination_necessary = False
                        saving_data = self.primary_data
                        #print(saving_data[0])
                    elif file_determination_formatted == 3:
                        active = True
                        data_determination_necessary = False
                        saving_data = self.processed_advertisement_data
                    else:
                        data_determination_necessary = True

                except:
                    print("please provide a number!")
                    data_determination_necessary = True

            while active:
                self.output_filename_user_input = input("filename?: ")
                if len(self.output_filename_user_input) < 1:
                    print("Invalid input")
                    continue
                else:
                    output_filename = self.output_filename_user_input + ".json"
                    break

            while active:
                file_location_name = "/Users/attilakiss/Desktop/project_HaHU_KA/Project-HaHU_KA/JSON_files/" + output_filename
                with open (file_location_name, 'w') as f_object:
                    #print(saving_data[0])
                    json.dump(saving_data, f_object)
                    f_object.close()
                    print("data has been written into '", output_filename,"'")
                    active = False

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
                counter = 0
                utag_data_attributes_raw = list()
                for i in self.utag_data:  #raw format utag_data; attributes had been not selected
                    if re.search(self.advertisement_attributes[counter], i):  #looping through the raw utag_data and find those which relevant in terms of attributes
                        utag_data_attributes_raw.append(i)
                        counter += 1
                        if counter == len(self.advertisement_attributes):    break  #handles out of index error

                attributes_dict_raw = dict()
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
            catalog_exclude2 = 'https://katalogus.hasznaltauto.hu/' + (self.processed_advertisement_data['brand']).lower() + '/' + (self.processed_advertisement_data['model']).lower() #the manucaturer and the model should be added to the URL
            if var_utag_data:
                try:
                    line_key = self.line_keys[2]
                    catalog_url_list = list()
                    for line in self.raw_lines:
                        if line_key in line:
                            catalog_url_list.append(re.findall('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+',line))  #looking for an URL link, usually finds three

                    #Enhancement point 2: exculding the non-relevant catalog URLs
                    for catalog_url in catalog_url_list:
                        if catalog_url == catalog_exclude1:
                            catalog_url_list.pop(catalog_url_list.index(catalog_exclude1))  #if the URL is a link to the main site of the catalog data, the result will be remove from the list

                        elif catalog_url == catalog_exclude2:
                            catalog_url_list.pop(catalog_url_list.index(catalog_exclude2))  #if the URL is a link to the car's main site of the catalog data, the result will be remove from the list
                        else:
                            self.catalog_url = catalog_url_list[0]

                except:
                    print("no relevant catalog url had been found")
                    cat_url = False


            #compiling the primary data into a dictionary
            if var_utag_data:
                self.primary_data['utag_data'] = self.utag_data
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
                self.primary_data['description'] = "no catalog"  #if no relevant catalog data had been found "no catalog" will be saved as an explanation

        else:
            print("no url for downloanding")
            self.processing = False
