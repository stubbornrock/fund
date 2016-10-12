# -*- coding: utf-8 -*-

class Model:
    def __init__(self):
        self.name = "No"
        self.evaluate_value = 0.0
        self.increase_value = 0.0
        self.increase_percent = 0.0
        self.per_value = 0.0
        self.per_value_percent = 0.0
        self.total_value = 0.0
        self.wan_get = 0.0
        self.seven_get = 0.0
        self.fourting_get = 0.0
        self.two_eghit_get = 0.0
        self.one_month = 0.0
        self.three_month = 0.0
        self.six_month = 0.0
        self.one_year = 0.0
        self.three_year = 0.0
        self.till_now = 0.0
        self.type = 0.0
        self.size = 0.0
        self.manager = 0.0
        self.start_date = 0.0 
        self.owner = 0.0
        self.level = 0.0
        self.updated = True
        self.code = '000001'
    def get_model_tuple(self):
        return (self.name,self.evaluate_value,self.increase_value,self.increase_percent,\
                self.per_value,self.per_value_percent,self.total_value,\
                self.wan_get,self.seven_get,self.fourting_get,self.two_eghit_get,\
                self.one_month,self.three_month,self.six_month,self.one_year,self.three_year,self.till_now,\
                self.type,self.size,self.manager,self.start_date,self.owner,self.level,self.updated,\
                self.code)

SQL = "UPDATE fund SET name = %s, evaluate_value = %s, increase_value = %s,increase_percent = %s,\
per_value = %s, per_value_percent = %s, total_value = %s,\
wan_get = %s, seven_get = %s, fourting_get = %s, two_eghit_get = %s,\
one_month = %s,three_month = %s,six_month = %s,one_year = %s,three_year = %s,till_now = %s,\
type = %s,size = %s, manager = %s,start_date = %s,owner = %s,level = %s,updated = %s\
WHERE code = %s;"

if __name__ == '__main__':
    m = Model()
    print m.get_model_tuple()
