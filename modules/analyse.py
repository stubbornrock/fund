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
    sql="select code,owner,name,level from fund where type like '%s' order by %s desc limit %s;" %(type,field,count)
    infos = my.get_datas(sql)
    return infos

def analyse_percent(end):
    type="%混合%"
    count="50"
    codes={}
    funds=[]
    time="+".join(FIELDS[0:end])
    result=set()
    for field in FIELDS[0:end]:
        infos = query_infos(type,count,field)
        #funds
        for info in infos:
            fund={}
            fund['code']=info[0]
            fund['owner']=info[1]
            fund['name']=info[2]
            fund['level']=info[3]
            funds.append(fund)
        #codes
        cs = [info[0] for info in infos]
        codes[field]=cs
    for field in FIELDS[0:end]:
        if result:
            result = result & set(codes[field])
        else:
            result = set(codes[field])
    print "############ %50s #############" %time
    for r in list(result):
        for f in funds:
            if f['code'] == r:
                print "CODE:%-6s  NAME:%-30s  LEVEL:%-5s  OWNER:%-30s" %(f['code'],f['name'],f['level'],f['owner'])
                break
analyse_percent(1)
analyse_percent(2)
analyse_percent(3)
analyse_percent(4)
analyse_percent(5)
print ""
print ""

def analyse_owners(end):
    type="%混合%"
    count="50"
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
