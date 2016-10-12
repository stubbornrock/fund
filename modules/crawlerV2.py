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
from common import Model,SQL

WEB_URL="http://fund.eastmoney.com/"

def exec_shell_result(cmd):
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    return_code = p.wait()
    result = None
    if return_code == 0:
        result = p.stdout.readline().strip()
    else:
        LOG.error("host exec subbprocess < %s >error!" %cmd)
    return result

def prase_content(soup):
    model = Model()
    try:
        title = soup.find("title")
        model.name = title.text.split('(')[0]

        item01 = soup.find("dl",class_="dataItem01")
        model.evaluate_value = item01.contents[1].contents[0].text
        model.increase_value = item01.contents[1].contents[2].contents[0].text
        model.increase_percent = item01.contents[1].contents[2].contents[1].text[:-1]
        model.one_month = item01.contents[2].contents[1].text[:-1]
        model.one_year = item01.contents[3].contents[1].text[:-1]

        item02 = soup.find("dl",class_="dataItem02")
        model.per_value = item02.contents[1].contents[0].text
        model.per_value_percent = item02.contents[1].contents[1].text[:-1]
        model.three_month = item02.contents[2].contents[1].text[:-1]
        model.three_year = item02.contents[3].contents[1].text[:-1]

        item03 = soup.find("dl",class_="dataItem03")
        model.total_value = item03.contents[1].contents[0].text
        model.six_month = item03.contents[2].contents[1].text[:-1]
        model.till_now = item03.contents[3].contents[1].text[:-1]

        tables = soup.find_all("table")
        model.type = tables[2].contents[0].contents[0].text.split("|")[0]
        model.size = tables[2].contents[0].contents[1].contents[1][1:]
        model.manager = tables[2].contents[0].contents[2].contents[1].text
        model.start_date = tables[2].contents[1].contents[0].contents[1][1:]
        model.owner = tables[2].contents[1].contents[1].contents[2].text
        #model.level = tables[2].contents[1].contents[2].contents[2].text
        level = tables[2].contents[1].contents[2].contents[2].attrs['class'][0]
        if len(level) > 4:
            model.level = level[4]
        else:
            model.level = 0
    except IndexError,e:
        infoItem = soup.find("div",class_="fundInfoItem")
        model.wan_get = infoItem.contents[0].contents[0].contents[1].text
        model.seven_get = infoItem.contents[0].contents[2].contents[1].text[:-1]
        model.fourting_get = infoItem.contents[0].contents[4].contents[1].text[:-1]
        model.two_eghit_get = infoItem.contents[0].contents[6].contents[1].text[:-1]

        model.one_month = infoItem.contents[1].contents[0].contents[0].contents[1].text[:-1]
        model.one_year = infoItem.contents[1].contents[0].contents[1].contents[1].text[:-1]
        model.three_month = infoItem.contents[1].contents[1].contents[0].contents[1].text[:-1]
        model.three_year = infoItem.contents[1].contents[1].contents[1].contents[1].text[:-1]
        model.six_month = infoItem.contents[1].contents[2].contents[0].contents[1].text[:-1]
        model.till_now = infoItem.contents[1].contents[2].contents[1].contents[1].text[:-1]

        tables = soup.find_all("table")
        model.type = tables[2].contents[0].contents[0].text.split("|")[0]
        model.size = tables[2].contents[0].contents[1].contents[1][1:]
        model.manager = tables[2].contents[0].contents[2].contents[1].text
        model.start_date = tables[2].contents[1].contents[0].contents[1][1:]
        model.owner = tables[2].contents[1].contents[1].contents[2].text
        #model.level = tables[2].contents[1].contents[2].contents[2].text
        level = tables[2].contents[1].contents[2].contents[2].attrs['class'][0]
        if len(level) > 4:
            model.level = level[4]
        else:
            model.level = 0
    except Exception,e:
        #logger.error("%s => CONTENT PRASE FAIL :%s" %(url,str(e)))
        model = None
    else:
        attrs = model.__dict__
        for key in attrs.keys():
            if attrs[key] in [""," ","-","--"]:
                if key == "start_date":
                    model.start_date = "1900-00-00"
                else:
                    model.start_date = "0.0"
    return model

def fetch(start,end,thread_name,logger):
    my = MYSQL(thread_name)
    update_sql = "UPDATE fund SET updated=False WHERE code=%s;"
    code_set = codes[start:end]
    logger.info("%s => START  CLEAR UPDATED FIELD!" %thread_name)
    my.update_many_data(update_sql,code_set)
    logger.info("%s => FINISH CLEAR UPDATED FIELD!" %thread_name)
    
    logger.info("%s => START CRAWLER URLS DATA!" %thread_name)
    datas = []
    counter = 1
    for code in codes[start:end]:
        logger.info("%s => %s => %s START PRASE DATA ..." %(thread_name,counter,code))
        time.sleep(1)
        url="%s%s.html" %(WEB_URL,code)
        ##value
        try:
            body = urllib2.urlopen(url).read()
            soup = BeautifulSoup(body,"lxml")
        except Exception,e:
            logger.error("%s => %s => %s URL OPEN FAIL :%s" %(thread_name,counter,code,str(e)))
        else:
            model = prase_content(soup)
            ## append data
            if model: 
                datas.append(model.get_model_tuple())
            else:
                logger.error("%s => %s => %s START PRASE DATA FAIL ..." %(thread_name,counter,code))
        finally:
            counter = counter + 1
    logger.info("%s => FINISH CRAWLER URLS DATA!" %thread_name)
    try:
        logger.info("%s => START UPDATE DATABSE ..." %thread_name)
        my.update_many_data(SQL,datas)
    except Exception,e:                
        logger.error("%s => UPDATE DATABSE FAIL :%s" %(thread_name,str(e)))
    finally:
        logger.info("%s => UPDATE DATABSE FINISH!!!!" %thread_name)
        my.close()

if __name__ == '__main__':
    style = sys.argv[1]
    codes = []
    if style == "all":
        main_sl =  MYSQL("main")
        codes = main_sl.get_datas("select code from fund;") 
        codes = [code[0] for code in codes]
        main_sl.close()
    elif style == "patch":
        patch_sl =  MYSQL("patch")
        codes = patch_sl.get_datas("select code from fund where updated=False;")
        codes = [code[0] for code in codes]
        patch_sl.close()
    elif style == "one":
        code = sys.argv[2]
        codes.append(code)

    total = len(codes)
    threads = []
    exec_shell_result("rm -rf /var/log/crawler/*.*")
    for i in range(100):
        my_codes_start=i*100
        my_codes_end=i*100+100
   
        start = 0
        end = 0
        if my_codes_start <= total:
            start = my_codes_start
            if my_codes_end <= total:
                end = my_codes_end
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
