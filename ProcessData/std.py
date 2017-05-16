import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import datetime

class StandardDeviation:
	path='./data'
	data={}

	def openFile(self):
		print ("open")
		for filename in os.listdir(self.path):
			self.readFile(filename)
			print(filename)
			self.data={}

	def readFile(self,filename):
		print("READ FILE")

			
if __name__=='__main__':
	std=StandardDeviation()
	std.openFile()
