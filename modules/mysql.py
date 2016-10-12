# -*- coding: utf-8 -*- 
import MySQLdb

class MYSQL:
    def __init__(self,client):
        self.client = client
        self.conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='fund')
        self.cursor = self.conn.cursor()
        self.conn.set_character_set('utf8')
        self.cursor.execute('SET NAMES utf8;') 
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')

    def get_datas(self,sql):
        self.cursor.execute(sql)
        alldata = self.cursor.fetchall()
        return alldata

    def get_one_data(self,sql):
        self.cursor.execute(sql)
        onedata = self.cursor.fetchone()
        return onedata

    def insert_data(self,sql):
        self.cursor.execute(sql)
        #self.conn.commit()

    def insert_many_data(self,sql,data):
        self.cursor.executemany(sql,data)
        self.conn.commit()
        
    def update_many_data(self,sql,data):
        self.cursor.executemany(sql,data)
        self.conn.commit()

    def update_data(self,sql):
        self.cursor.execute(sql)
        self.conn.commit()

    def create_table(self,sql):
        self.cursor.execute(sql)

    def close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    TABLE='''CREATE TABLE fund (
             ID int(50) NOT NULL auto_increment,
             code varchar(200) NOT NULL,
             name varchar(200),
             evaluate_value  decimal(16,4),
             increase_value  decimal(16,4),
             increase_percent decimal(16,4),
             wan_get decimal(16,4),
             seven_get decimal(16,4),
             fourting_get decimal(16,4),
             two_eghit_get decimal(16,4),
             per_value decimal(16,4),
             per_value_percent decimal(16,4),
             total_value decimal(16,4),
             one_month decimal(16,4),
             three_month decimal(16,4),
             six_month decimal(16,4),
             one_year decimal(16,4),
             three_year decimal(16,4),
             till_now decimal(16,4),
             type varchar(200),
             size varchar(200),
             manager varchar(200),
             start_date DATE,
             owner varchar(200),
             level int(4),
             url varchar(200),
             updated tinyint(1) default 0,
             PRIMARY KEY (`id`)
         );'''
    db = MYSQL("mine")
    try:
        print " >> MYSQL => Create fund table ..."
        db.create_table(TABLE)
    except Exception,e:
        print " >> MYSQL => %s ..." %str(e)
    else:
        print " >> MYSQL => Create fund table Success!"
    finally:
        db.close()
