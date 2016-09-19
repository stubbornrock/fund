#!/usr/bin/env python
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

def exec_shell_result(cmd):
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    return_code = p.wait()
    result = None
    if return_code == 0:
        result = p.stdout.readline().strip()
    else:
        LOG.error("host exec subbprocess < %s >error!" %cmd)
    return result

model={'evaluate_value':0.0,
       'increase_value':0.0,
       'increase_percent':0.0,
       'per_value':0.0,
       'per_value_percent':0.0,
       'total_value':0.0,
       'wan_get':0.0,
       'seven_get':0.0,
       'fourting_get':0.0,
       'two_eghit_get':0.0,
       'one_month':0.0,
       'three_month':0.0,
       'six_month':0.0,
       'one_year':0.0,
       'three_year':0.0,
       'till_now':0.0,
       'type':0.0,
       'size':0.0,
       'manager':0.0,
       'start_date':0.0,
       'owner':0.0,
       'level':0.0}

def fetch(start,end,thread_name,logger):
    my = MYSQL(thread_name)
    for url in urls[start:end]:
        time.sleep(1)
        ##value
        try: 
            body = urllib2.urlopen(url).read()
            soup = BeautifulSoup(body,"lxml")
        except Exception,e:
            logger.error("%s => FAIL :%s" %(url,str(e)))
        else:
            try:
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
                #model['level'] = tables[2].contents[1].contents[2].contents[2].text
                level = tables[2].contents[1].contents[2].contents[2].attrs['class'][0]
                if len(level) > 4:
                    model['level'] = level[4]
                else:
                    model['level'] = 0
            except IndexError,e:
                infoItem = soup.find("div",class_="fundInfoItem")
                model['wan_get'] = infoItem.contents[0].contents[0].contents[1].text
                model['seven_get'] = infoItem.contents[0].contents[2].contents[1].text[:-1]
                model['fourting_get'] = infoItem.contents[0].contents[4].contents[1].text[:-1]
                model['two_eghit_get'] = infoItem.contents[0].contents[6].contents[1].text[:-1]
                
                model['one_month'] = infoItem.contents[1].contents[0].contents[0].contents[1].text[:-1]
                model['one_year'] = infoItem.contents[1].contents[0].contents[1].contents[1].text[:-1]
                model['three_month'] = infoItem.contents[1].contents[1].contents[0].contents[1].text[:-1]
                model['three_year'] = infoItem.contents[1].contents[1].contents[1].contents[1].text[:-1]
                model['six_month'] = infoItem.contents[1].contents[2].contents[0].contents[1].text[:-1]
                model['till_now'] = infoItem.contents[1].contents[2].contents[1].contents[1].text[:-1]
                
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
            except Exception,e:
                logger.error("%s => FAIL :%s" %(url,str(e)))
            finally:
                for key in model.keys():
                    if model[key] in [""," ","-","--"]:
                        if key == "start_date":
                            model[key] = "1900-00-00"
                        else:
                            model[key] = "0.0"
                sql='''UPDATE fund SET evaluate_value = %s,
                                   increase_value = %s,
                                   increase_percent = %s,
                                   per_value = %s,
                                   per_value_percent = %s,
                                   total_value = %s,
                                   wan_get = %s,
                                   seven_get = %s,
                                   fourting_get = %s,
                                   two_eghit_get = %s,
                                   one_month = %s,
                                   three_month = %s,
                                   six_month = %s,
                                   one_year = %s,
                                   three_year = %s,
                                   till_now = %s,
                                   type = "%s",
                                   size = "%s",
                                   manager = "%s",
                                   start_date = "%s",
                                   owner = "%s",
                                   level = "%s"
                       WHERE url="%s";'''%(model['evaluate_value'],model['increase_value'],model['increase_percent'],
                                           model['per_value'],model['per_value_percent'],model['total_value'],
                                           model['wan_get'],model['seven_get'],model['fourting_get'],model['two_eghit_get'],
                                           model['one_month'],model['three_month'],model['six_month'],
                                           model['one_year'],model['three_year'],model['till_now'],
                                           model['type'],model['size'],model['manager'],
                                           model['start_date'],model['owner'],model['level'],
                                           url)
                ## insert data
                try:
                    my.insert_data(sql)
                except Exception,e:
                    logger.error("%s => FAIL :%s" %(url,str(e)))
                else:
                    logger.debug("%s => OK" %url)
    my.close()

if __name__ == '__main__':
    style = sys.argv[1]
    urls = []
    if style == "all":
        main_sl =  MYSQL("main")
        us = main_sl.get_datas("select url from fund;") 
        urls = [url[0] for url in us]
        main_sl.close()
    elif style == "patch":
        urls = check(True)
    elif style == "one":
        url = sys.argv[2]
        urls.append(url)

    total = len(urls)
    threads = []
    exec_shell_result("rm -rf /var/log/crawler/*.*")
    for i in range(100):
        my_urls_start=i*100
        my_urls_end=i*100+100
   
        start = 0
        end = 0
        if my_urls_start <= total:
            start = my_urls_start
            if my_urls_end <= total:
                end = my_urls_end
            else:
                end = total
        else:
            break
        thread_name = "thread_%s->%s" %(start,end)
        logger = LOG(thread_name)
        mylogger = logger.get_logger()
        th = threading.Thread(name=thread_name,target=fetch,args=(start,end,thread_name,mylogger))
        threads.append(th)

    for t in threads:
        t.start()
    while True:
        th_num = threading.activeCount() - 1
        #print "Current Has %d threads active crawlering datas waiting ..." %th_num
        #current_th_names = [item.name for item in threading.enumerate() if item.name !='MainThread']
        if th_num == 0:
            break
        time.sleep(30)
    #print "Finshed!"
