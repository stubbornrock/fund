# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import sqlite3
import re
from mysql import MYSQL

WEB_URL="http://fund.eastmoney.com/"

my = MYSQL("pull")
fo=open("./allfund.html").read()
regex = re.compile("href=\"http://fund.eastmoney.com/\d+.html")
funds=re.findall(regex,fo)
for f in funds:
    code=f.split("/")[3][:-5]
    url="%s%s.html" %(WEB_URL,code)
    sql='''SELECT count(*) FROM fund WHERE code="%s";''' %code
    total=my.get_one_data(sql)
    if total[0] == 1:
        sql='''UPDATE fund SET url="%s" WHERE code="%s";''' %(url,code)
    else:
        sql='''INSERT INTO fund (code,name,url) VALUES ("%s","%s","%s");''' %(code,'No',url)
    my.insert_data(sql)
my.close()
print " >> Records created successfully";
