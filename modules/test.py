<<<<<<< HEAD
from bs4 import BeautifulSoup
import urllib2
import sqlite3
import re
import threading
from mysql import MYSQL
from patch import check
from log import LOG
import time
import subprocess
import sys
url="http://fund.eastmoney.com/000263.html"
body = urllib2.urlopen(url).read()
soup = BeautifulSoup(body,"lxml")
model={}

title = soup.find("title")
model['name']=title.text.split('(')[0]
item01 = soup.find("dl",class_="dataItem01")
model['evaluate_value'] = item01.contents[1].contents[0].text
model['increase_value'] = item01.contents[1].contents[2].contents[0].text
model['increase_percent'] = item01.contents[1].contents[2].contents[1].text[:-1]
model['one_month'] = item01.contents[2].contents[1].text[:-1]
model['one_year'] = item01.contents[3].contents[1].text[:-1]
=======
fields=["one_month","three_month","six_month","one_year","three_year"]
print fields[0:3]

>>>>>>> 82d399de5e7df5318209f2ae1b9297ac155294a1

a=[1,2,3]
b=[]
print list(set(a) & set(b))

<<<<<<< HEAD
item03 = soup.find("dl",class_="dataItem03")
model['total_value'] = item03.contents[1].contents[0].text
model['six_month'] = item03.contents[2].contents[1].text[:-1]
model['till_now'] = item03.contents[3].contents[1].text[:-1]

tables = soup.find_all("table")
model['type'] = tables[2].contents[0].contents[0].text.split("|")[0]
model['size'] = tables[2].contents[0].contents[1].contents[1][1:]
model['manager'] = tables[2].contents[0].contents[2].contents[1].text
model['start_date'] = tables[2].contents[1].contents[0].contents[1][1:]
model['owner'] = tables[2].contents[1].contents[1].contents[2].text
#model['level'] = tables[2].contents[1].contents[2].contents[2].text
level = tables[2].contents[1].contents[2].contents[2].attrs['class'][0]
if len(level) > 4:
    model['level'] = level[4]
else:
    model['level'] = 0

for key in model.keys():
    print "%20s => %s" %(key,model[key])
=======
c=set()
if c:
   print "lala"
else:
   print "kong"
>>>>>>> 82d399de5e7df5318209f2ae1b9297ac155294a1
