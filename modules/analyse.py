# -*- coding: utf-8 -*-
from mysql import MYSQL
my = MYSQL("analyse")

type="%混合%"
count="30"
field="one_month"
sql="select code from fund where type like '%s' order by %s desc limit %s;" %(type,field,count)
m1s = my.get_datas(sql)
m1s = [m1[0] for m1 in m1s]

field="three_month"
sql="select code from fund where type like '%s' order by %s desc limit %s;" %(type,field,count)
m3s = my.get_datas(sql)
m3s = [m3[0] for m3 in m3s]

field="six_month"
sql="select code from fund where type like '%s' order by %s desc limit %s;" %(type,field,count)
m6s = my.get_datas(sql)
m6s = [m6[0] for m6 in m6s]


field="one_year"
sql="select code from fund where type like '%s' order by %s desc limit %s;" %(type,field,count)
y1s = my.get_datas(sql)
y1s = [y1[0] for y1 in y1s]

field="three_year"
sql="select code from fund where type like '%s' order by %s desc limit %s;" %(type,field,count)
y3s = my.get_datas(sql)
y3s = [y3[0] for y3 in y3s]

my.close()

m136s = list(set(m1s) & set(m3s) & set(m6s))
m136y1s = list(set(m1s) & set(m3s) & set(m6s) & set(y1s))
alls = list(set(m1s) & set(m3s) & set(m6s) & set(y1s) & set(y3s))
print "1,3,6 months: %s" %m136s
print "1,3,6 months 1 years: %s" %m136y1s
print "1,3,6 months 1,3 years: %s" %alls





