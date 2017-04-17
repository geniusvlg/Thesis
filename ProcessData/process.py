import os
import json

class ProcessData:

	path='./data'
	output={}
	def openFile(self):
		for filename in os.listdir(self.path):
			self.readFile(filename)

	def readFile(self,filename):
		with open(self.path+'/'+filename,'r') as f:
			ite=0
			for line in f:
				print('Processing item {}'.format(ite+1))
				ite+=1
				item=json.loads(line)
				if self.output.get(item['location']['province'])==None:
					self.output[item['location']['province']]={}
				byProvince=self.output[item['location']['province']]
				if byProvince.get(item['location']['county'])==None:
					byProvince[item['location']['county']]={}
				byCounty=byProvince[item['location']['county']]
				if byCounty.get(item['house-type']['detailed'])==None:
					byCounty[item['house-type']['detailed']]=[]
				container=byCounty[item['house-type']['detailed']]
				container.append(item)

			self.printOutput(filename)

	def printOutput(self,filename):
		with open(filename+'output.json','w') as f:
			json.dump(self.output,f,indent=4,separators=(',',': '),sort_keys=True)

if __name__=='__main__':
	pdata=ProcessData()
	pdata.openFile()
