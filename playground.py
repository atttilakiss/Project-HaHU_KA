

# standard modules
import json
import urllib.request, urllib.parse, urllib.error
import sqlite3
import re
import sys
from datetime import *


init_url = 'https://www.hasznaltauto.hu/szemelyauto/skoda/superb/skoda_superb_1_8_tsi_lk-15318038'
class URl_collect_test:
    def __init__(self, init_url):
        self.input_url = init_url
        self.raw_lines = list()
        self.striped_lines = list()

    def page_download(self):
        fhand = urllib.request.urlopen(self.input_url)
        for line in fhand:
            self.raw_lines.append(line.decode().strip())

        print(type(self.raw_lines))
        return self.raw_lines

class PageDownload:
    def __init__(self):
        self.page_url_link = str()
        self.raw_page = str()
        self.raw_lines = list()

    def URL_raw_download(self):
        input_url = input("please paste the url: ")
        file_handler = urllib.request.urlopen(input_url)
        for line in file_handler:
            self.raw_page.append(line)

        return self.raw_page

"""
test_url = URl_collect_test(init_url)

collected_url = list()
collected_url = test_url.page_download()

for i in collected_url:
    print(i)
"""

test_url = PageDownload()
result = test_url.URL_raw_download()
print(type(result))
print(result)
