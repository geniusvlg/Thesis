import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import datetime
import math

class StandardDeviation:
	data={}
	data_path = './processed'
	store_path = './remove_outlier'

	def openFile(self):
		for filename in os.listdir(self.data_path):
			self.readFile(filename)
			print(filename)

	def readFile(self,filename):
		with open(self.data_path + '/' + filename,'r+') as f:
			data = json.load(f)
			for province in data:
				for county in data[province]:
					for house_type in data[province][county]:
						mean = self.calMean(data[province][county][house_type])
						standard = self.calStd(data[province][county][house_type], mean)
						for item in data[province][county][house_type]:
							if item.get("price") < (mean - 3*standard) or item.get("price") > (mean + 3*standard):
								data[province][county][house_type].remove(item)
		with open(self.store_path + '/' + filename, 'w') as f:
			json.dump(data,f)			
			
	def calMean(self,list):
		total = 0
		for item in list:
			total = total + item.get("price")
		return total / len(list)

	def calStd(self, list, mean):
		if len(list) == 1:
			return 0
		total = 0
		variance = 0
		for item in list:
			variance  = variance + math.pow((item.get("price") - mean),2)
		variance = variance / len(list)
		return math.sqrt(variance)
	
if __name__=='__main__':
	std=StandardDeviation()
	std.openFile()