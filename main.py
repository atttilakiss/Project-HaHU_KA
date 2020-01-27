#2020_01_22

# standard modules
import json
import urllib.request, urllib.parse, urllib.error
import sqlite3
import re
import sys
from datetime import *
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

# developed modules
from url_collect_class import *
from url_collect_class_regex import *


car_page = PageDownload()  #creating an instance of the PageDownload class

car_page.URL_prompt()  #method that is asking for an URL;currently disabled 2020_01_23
car_page.URL_raw_download()  #downloading the page in raw HTML5 format
car_page.primary_data_retrieve()  #gathering the primary data from the downloaded raw HTML5 page
car_page.json_file_saving()  #asking the user about the saving possibility
