#2020_01_23

# standard modules
import json
import urllib.request, urllib.parse, urllib.error
import sqlite3
import re
import sys
from datetime import *


class PageDownload:
    def __init__(self):
        self.page_url_link = str()
        self.raw_lines = list()
        self.output_filename_user_input = str()
        self.output_filename = str()

        self.line_keys = ['var utag_data', 'Leírás', 'katalogus']
        self.utag_data = list()
        self.description = str()
        self.catalog_url = str()
        self.primary_data = dict()


    def URL_prompt(self):
        """
        prompt an URL for downloading
        """
        #self.page_url_link = input("please paste the url: ")
        self.page_url_link = 'https://www.hasznaltauto.hu/kishaszonjarmu/ford/transit/ford_transit_2_4_tdci_350_jumbo_el_duplakerek_emelohatfal_vonohorog_klima_tempomat-15328235'
        #enhancement: URL format testing with regex 2020_01_23


    def URL_raw_download(self):
        """
        downloading the page of the provided URL;
        very raw format
        return is a list with the full HTML page
        """
        file_handler = urllib.request.urlopen(self.page_url_link)
        for line in file_handler:
            self.raw_lines.append(line.decode().strip())


    def json_file_saving(self):
        """
        saving the provided dataset in JSON format
        saved data can be selected
        exception handling had been impemented
        """
        saving = input("Do you wanna save results in JSON?")
        if len(saving) == 0:
            active = False
            data_determination = False
        else:
            active = True
            data_determination = True

        while data_determination:
            print("what data would you like to save?\n1 - raw_lines\n2 - primary_data")
            file_determination = input("Hit Enter for no saving; provide number: ")

            try:
                if len(file_determination) == 0:
                    active = False
                    break
                file_determination_formatted = int(file_determination)
                if len(file_determination) == 0:
                    active = False
                    data_determination = False
                    break
                elif file_determination_formatted == 1:
                    active = True
                    data_determination = False
                    saving_data = self.raw_lines
                    #print(saving_data[0])
                elif file_determination_formatted == 2:
                    active = True
                    data_determination = False
                    saving_data = self.primary_data
                    #print(saving_data[0])

                else:
                    data_determination = True

            except:
                print("please provide a number!")
                data_determination = True

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



    def primary_data_retrieve(self):
        """
        gathering the utag data from the raw HTML5 data
        gathering the description from the raw HTML5 data
        gathering the catalog URL link from the raw HTML5 data
        """

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

        #Enhancement point: regex alanysis of utag_data

        except:
            print("no 'var utag_data' had been found")
            var_utag_data = False  #if no var utag_data found it stops running


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
        if var_utag_data:
            try:
                line_key = self.line_keys[2]
                catalog_url_list = list()
                for line in self.raw_lines:
                    if line_key in line:
                        catalog_url_list.append(re.findall('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+',line))  #looking for an URL link, usually finds three

                self.catalog_url = max(catalog_url_list, key = len)  #selects the longest URL fromt he found ones

                #Enhancement point: exculding the non-relevant catalog URLs

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
