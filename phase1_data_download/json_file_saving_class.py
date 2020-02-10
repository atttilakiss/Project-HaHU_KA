import json
import urllib.request, urllib.parse, urllib.error
import sqlite3
import re
import sys
from datetime import *
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class JSON_saving:
    def __init__(self):
        self.output_filename_user_input = str()

    def json_saving(self, advertisement_data, catalog_data, full_data):
        saving = input("Do you wanna save results in JSON?")
        if len(saving) == 0:
            active = False
            data_determination_necessary = False
        else:
            active = True
            data_determination_necessary = True

        while data_determination_necessary:
            print("what data would you like to save?\n1 - advertisement_data\n2 - catalog_data\n3 - full_data")
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
                    saving_data = advertisement_data
                    #print(saving_data[0])
                elif file_determination_formatted == 2:
                    active = True
                    data_determination_necessary = False
                    saving_data = catalog_data
                    #print(saving_data[0])
                elif file_determination_formatted == 3:
                    active = True
                    data_determination_necessary = False
                    saving_data = full_data
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
