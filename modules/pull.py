# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import sqlite3
import re
from mysql import MYSQL

WEB_URL="http://fund.eastmoney.com/"

fo=open("./allfund.html").read()
regex = re.compile("href=\"http://fund.eastmoney.com/\d+.html")
funds=re.findall(regex,fo)
web_codes = [f.split("/")[3][:-5] for f in funds]
web_codes = list(set(web_codes))
print " >> %4s codes pull from web page !" %len(web_codes)

my = MYSQL("pull")
db_codes_sql = '''select code from fund;'''
db_codes = my.get_datas(db_codes_sql)
db_codes = [ code[0] for code in db_codes]
print " >> %4s codes in Database fund !" %len(db_codes)

data_update = []
data_insert = []
for code in web_codes:
    url="%s%s.html" %(WEB_URL,code)
    if code not in db_codes:
        i=(code,url)
        data_insert.append(i)
    else:
        u=('niuniu',code)
        data_update.append(u)
print " >> %4s codes need insert into Database fund !" %len(data_insert)
print " >> %4s codes need update into Database fund !" %len(data_update)

if data_insert:
    insert_sql = "INSERT INTO fund(code,url) VALUES (%s,%s);"
    my.insert_many_data(insert_sql,data_insert)

#if data_update:
#    update_sql = "UPDATE fund SET name=%s WHERE code=%s;"
#    my.insert_many_data(update_sql,data_update)
my.close()
