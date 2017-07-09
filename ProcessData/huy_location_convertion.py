import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import datetime
import math

class LocationConversion:
	data = {}
	data_path = './data'

	def openFile(self):
		self.keywords = ['quan','huyen','thanh pho', 'thi xa', 'phuong', 'xa', 'thi tran']
		for filename in os.listdir(self.data_path):
			self.convertLocation(filename)

	def convertLocation(self,filename):
		with open(self.data_path + '/' + filename,'r') as f:
			for line in f:
				item=json.loads(line)
				self.convertItem(item['location']['province'])
				self.convertItem(item['location']['county'])
				self.convertItem(item['location']['ward'])

	def convertItem(self, item):
		item = item.lower()
		print (item)
		for word in self.keywords:
			if (item.find(word) == 0) or ("tp." in item):
				item_list = item.split()
				if item_list[1].isdigit() == False:
					if "tp." in item:
						item = item.replace("tp.","")
					else:
						item = item.replace(word + " ","")
		print (item)

if __name__ =='__main__':
	lc = LocationConversion()
	lc.openFile()
