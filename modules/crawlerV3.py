# -*- coding: utf-8 -*-
#!/usr/bin/env python
from bs4 import BeautifulSoup
import urllib2
import sqlite3
import re
from multiprocessing import Pool
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

def prase_content(soup,code):
    model = Model()
    model.code = unicode(code,"utf-8")
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
    finally:
        if model:
            attrs = model.__dict__
            for key in attrs.keys():
                if attrs[key] in [u'',u' ',u'-',u'--']:
                    if key == "start_date":
                        model.start_date = "1900-00-00"
                    else:
                        setattr(model,key,"0.0")
                if key == 'increase_value':
                    value = str(attrs[key])
                    if '+-' in value:
                        l = len(attrs[key])
                        value = attrs[key][1:l]
                        setattr(model,key,float(value))
    return model

def thread_fetch(thread_codes,thread_name,logger):
    my = MYSQL(thread_name)
    update_sql = "UPDATE fund SET updated=False WHERE code=%s;"
    code_set = thread_codes
    logger.info("%s => START  CLEAR UPDATED FIELD!" %thread_name)
    my.update_many_data(update_sql,code_set)
    logger.info("%s => FINISH CLEAR UPDATED FIELD!" %thread_name)
    
    logger.info("%s => START CRAWLER URLS DATA!" %thread_name)
    datas = []
    counter = 1
    for code in thread_codes:
        logger.info("%s => %s => ** %s ** START PRASE DATA ..." %(thread_name,counter,code))
        time.sleep(1)
        url="%s%s.html" %(WEB_URL,code)
        ##value
        try:
            body = urllib2.urlopen(url).read()
            soup = BeautifulSoup(body,"lxml")
        except Exception,e:
            logger.error("%s => %s => ** %s ** URL OPEN FAIL :%s" %(thread_name,counter,code,str(e)))
        else:
            model = prase_content(soup,code)
            ## append data
            if model: 
                datas.append(model.get_model_tuple())
            else:
                logger.error("%s => %s => ** %s ** START PRASE DATA FAIL ..." %(thread_name,counter,code))
        finally:
            counter = counter + 1
    logger.info("%s => FINISH CRAWLER URLS DATA!" %thread_name)
    try:
        logger.info("%s => START UPDATE DATABSE ..." %thread_name)
        my.update_many_data(SQL,datas)
    except Exception,e:                
        logger.error("%s => UPDATE DATABSE FAIL :%s" %(thread_name,str(e)))
    else:
        logger.info("%s => UPDATE DATABSE SUCCESS!" %thread_name)
    finally:
        logger.info("%s => UPDATE DATABSE FINISH!!!!" %thread_name)
        my.close()

def process_fecth(process_name,process_codes):
    total = len(process_codes)
    threads = []
    THREAD_NUM = 30
    if (total % THREAD_NUM):
        count = (total/THREAD_NUM)+1
    else:
        count = (total/THREAD_NUM)
    #print "%s threads (%s) start ... each num: %s" %(process_name,count,THREAD_NUM)
    for i in range(count):
        thread_name = "%s_thread_%d" %(process_name,i)
        thread_codes_start=i*THREAD_NUM
        thread_codes_end=i*THREAD_NUM+THREAD_NUM
        start = 0
        end = 0
        if thread_codes_start <= total:
            start = thread_codes_start
            if thread_codes_end <= total:
                end = thread_codes_end
            else:
                end = total
        thread_codes = process_codes[start:end]
        logger = LOG(thread_name)
        mylogger = logger.get_logger()
        th = threading.Thread(name=thread_name,target=thread_fetch,args=(thread_codes,thread_name,mylogger))
        threads.append(th)
        #print thread_name,len(thread_codes)
    for t in threads:
        t.start()
        t.join()
    #print "%s threads (%s) finish done ... " %(process_name,count)
    
def get_codes(style,c):
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
        code = c
        codes.append(code)
    return codes

if __name__ == '__main__':
    style = sys.argv[1]
    c = None
    if len(sys.argv) > 2:
        c = sys.argv[2]
    codes = get_codes(style,c)
    total = len(codes)
    exec_shell_result("rm -rf /var/log/crawler/*.*")

    ################################################
    p = Pool(50)
    PROCESS_NUM = 500
    if (total % PROCESS_NUM):
        count = (total/PROCESS_NUM)+1
    else:
        count = (total/PROCESS_NUM)
    print "All subprocess (%s) start ... each num: %s" %(count,PROCESS_NUM)
    for i in range(count):
        process_name = "process_%d" %i
        process_codes_start=i*PROCESS_NUM
        process_codes_end=i*PROCESS_NUM+PROCESS_NUM
        start = 0
        end = 0
        if process_codes_start <= total:
            start = process_codes_start
            if process_codes_end <= total:
                end = process_codes_end
            else:
                end = total
        process_codes = codes[start:end]
        p.apply_async(process_fecth,args=(process_name,process_codes,))
    p.close()
    p.join()
    print "All subprocesses (%s) finish done ..." %count
