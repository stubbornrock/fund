# -*- coding: utf-8 -*-
from mysql import MYSQL
import operator
my = MYSQL("analyse")
FIELDS=["one_month","three_month","six_month","one_year","three_year"]
def query_field(field,condition):
    sql="select %s from fund where %s;" %(field,condition)
    infos = my.get_datas(sql)
    return infos

def query_infos(type,count,field):
    sql="select code,owner from fund where type like '%s' order by %s desc limit %s;" %(type,field,count)
    infos = my.get_datas(sql)
    return infos

def analyse_percent(end):
    type="%混合%"
    count="30"
    codes={}
    funds={}
    time="+".join(FIELDS[0:end])
    result=set()
    for field in FIELDS[0:end]:
        infos = query_infos(type,count,field)
        cs = [info[0] for info in infos]
        codes[field]=cs
        for info in infos:
            if info[0] not in funds.keys():
                funds[info[0]]=info[1]
    for field in FIELDS[0:end]:
        if result:
            result = result & set(codes[field])
        else:
            result = set(codes[field])
    print "############ %s #############" %time
    for r in list(result):
        print "%s=>%s" %(r,funds[r])

analyse_percent(3)
analyse_percent(4)
analyse_percent(5)

def analyse_owners(end):
    type="%混合%"
    count="30"
    owners={}
    time="+".join(FIELDS[0:end])
    for field in FIELDS[0:end]:
        infos = query_infos(type,count,field)
        os = [info[1].strip() for info in infos]
        for owner in os:
            if owner in owners.keys():
               owners[owner]=owners[owner]+1
            else:
               owners[owner]=1
    owners = sorted(owners.iteritems(),key=operator.itemgetter(1),reverse=True)
    print "############ %s #############" %time
    for o in owners:
        print "%3s => %s" %(o[1],o[0])

analyse_owners(4)
