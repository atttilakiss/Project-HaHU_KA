#20200210

import urllib.request, urllib.error
import sqlite3
from datetime import *
import sys


def advert_url_query(cur):
    URL_query = list()
    advertisement_url_list = list()

    cur.execute("""SELECT advertisement_url FROM Advertisements WHERE status IS NULL OR status = 'OPEN'""")
    URL_query = cur.fetchall()
    #print(len(URL_query))
    for url in URL_query:
        advertisement_url_list.append(str(url[0]))
    
    
    #return advertisement_urls
    return advertisement_url_list

def advert_url_status_update(cur, advertisement_url_list, conn):
    #now = datetime.now()
    update_batch = int(input("how many advertisement should be updated?: "))
    for url in advertisement_url_list[:update_batch]:
        try:
            req = urllib.request.urlopen(url)
            print(req.code, url)
            
            load_data = list()
            load_data.append('99991231')
            load_data.append('OPEN')
            load_data.append(url)


            cur.execute("""UPDATE Advertisements 
                            SET sales_date = ?,
                                status = ?
                            WHERE advertisement_url = ? """, load_data)
        except urllib.error.HTTPError as e:
            print(e.code, url)

            load_data = list()
            load_data.append(datetime.now().strftime("%Y%m%d"))
            load_data.append('SOLD')
            load_data.append(url)

            cur.execute("""UPDATE Advertisements 
                            SET sales_date = ?,
                                status = ?
                            WHERE advertisement_url = ? """, load_data)

        conn.commit()

sql_database = '/Users/attilakiss/Desktop/project_HaHU_KA/Project-HaHU_KA/DB/test_db.db'
conn = sqlite3.connect(sql_database)
cur = conn.cursor()

test_url_query = advert_url_query(cur)
#print(len(test_url_query))
"""
for i in test_url_query[:10]:
    print(i)
"""

advert_url_status_update(cur, test_url_query, conn)

conn.close()
