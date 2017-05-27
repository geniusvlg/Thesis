from pymongo import MongoClient
import os
import json


class MongoWrite:
	data=[]
	def init(self):
		self.mongo=MongoClient()
		self.read_json()
		self.write_json()
	def read_json(self):
		with open('./processed/batdongsan.output.json') as f:
			data=json.load(f)
			self.read_leaf(data)

	def write_json(self):
		db=self.mongo['realestate']
		coll=db['houses']
		for item in self.data:
			result=coll.insert_one(item)

	def read_leaf(self,data):
		for k,v in data.items():
			if isinstance(v,dict):
				self.read_leaf(v)
			else:
				for item in v:
					self.data.append(item)

if __name__ == '__main__':
	obj=MongoWrite()
	obj.init()
