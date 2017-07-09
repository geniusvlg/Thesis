from pymongo import MongoClient
import os
import json
from datetime import datetime

def is_number(text):
    try:
        float(text)
        return True
    except ValueError:
        return False

class MongoWrite:
    data=[]
    def init(self):
        self.mongo=MongoClient("ds151232.mlab.com",51232)
        command= input("What do you want to write? ")
        self.read_json(command=='full')
        if command=='full':
            self.write_full()
        elif command =='time':
            self.write_time()

    def read_json(self,command):
        with open('./processed/merge_output_fix.json') as f:
            data=json.load(f)
            self.read_leaf(data,command)

    def write_full(self):
        db=self.mongo['realestate']
        db.authenticate('anvo','anvo')
        coll=db['houses']
        for item in self.data:
            del item['description']
            result=coll.insert_one(item)

    def write_time(self):
        db=self.mongo['realestate']
        coll=db['datevalues']
        for item in self.data:
            item['date']=datetime.strptime(item['date'],"%d-%m-%Y")
            result= coll.insert_one(item)
            


    def read_leaf(self,data,is_full):
        for k,v in data.items():
            if isinstance(v,dict):
                self.read_leaf(v,is_full)
            else:
                for item in v:
                    if (is_full):
                        item['post-time']['date']=datetime.strptime(item['post-time']['date'],"%d-%m-%Y")
                        self.data.append(item)
                    else:
                        if (not any(x['date'] == item['post-time']['date'] for x in self.data)):
                            self.data.append({"date":item['post-time']['date'],"count":1,"total":item['price']})
                        else:
                            date_item=[x for x in self.data if x['date']==item['post-time']['date']][0]
                            date_item['count']+=1
                            date_item['total']+=item['price']



if __name__ == '__main__':
    obj=MongoWrite()
    obj.init()
