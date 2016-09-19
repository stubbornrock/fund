from bs4 import BeautifulSoup
import urllib2
url="http://fund.eastmoney.com/160512.html"
body = urllib2.urlopen(url).read()
soup = BeautifulSoup(body,"lxml")
model = {}

item01 = soup.find("dl",class_="dataItem01")
model['evaluate_value'] = item01.contents[1].contents[0].text
model['increase_value'] = item01.contents[1].contents[2].contents[0].text
model['increase_percent'] = item01.contents[1].contents[2].contents[1].text[:-1]
model['one_month'] = item01.contents[2].contents[1].text[:-1]
model['one_year'] = item01.contents[3].contents[1].text[:-1]

item02 = soup.find("dl",class_="dataItem02")
model['per_value'] = item02.contents[1].contents[0].text
model['per_value_percent'] = item02.contents[1].contents[1].text[:-1]
model['three_month'] = item02.contents[2].contents[1].text[:-1]
model['three_year'] = item02.contents[3].contents[1].text[:-1]

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
level = tables[2].contents[1].contents[2].contents[2].attrs['class'][0]
if len(level) > 4:
    model['level']=level[4]
else:
    model['level']=0

print model['level']



