import os
import json

class StandardDeviation:
	path='./data'
	data={}

	def openFile(self):
		for filename in os.listdir(self.path):
			self.readFile(filename)
			print(filename)
			self.data={}

	def readFile(self, filename):
		with open(self.path+'/'+filename,'r') as f:
			for line in f:
				item=json.loads(line)
				print (item)

			
