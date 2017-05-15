import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import datetime

class ProcessData:

	path='./data'
	data={}
	def openFile(self):
		for filename in os.listdir(self.path):
			self.readFile(filename)
			print(filename)
			self.data={}

	def readFile(self,filename):
		with open(self.path+'/'+filename,'r') as f:
			ite=0
			for line in f:
				if ite%500==0:
					print('Processing item {}'.format(ite+1))
				ite+=1
				item=json.loads(line)
				if self.data.get(item['location']['province'])==None:
					self.data[item['location']['province']]={}
				byProvince=self.data[item['location']['province']]
				if byProvince.get(item['location']['county'])==None:
					byProvince[item['location']['county']]={}
				byCounty=byProvince[item['location']['county']]
				if byCounty.get(item['location']['ward'])==None:
					byCounty[item['location']['ward']]=[]
				byWard=byCounty[item['location']['ward']]
				if byWard.get(item['location']['road'])==None:
					byWard[item['location']['road']]=[]
				byRoad=byWard[item['location']['road']]
				if byRoad.get(item['house-type'])==None:
					byRoad[item['house-type']]=[]
				container=byRoad[item['house-type']]


				container.append(item)
			self.remove_duplication()
			self.printOutput(filename)

	def printOutput(self,filename):
		with open('./processed/'+filename[:-2]+'output.json','w') as f:
			print(len(self.data))
			json.dump(self.data,f,indent=4,separators=(',',': '),sort_keys=True)

	def remove_duplication(self):
		allcount=0
		with open('test.txt','w') as f:
			for province in self.data:
				for county in self.data[province]:
					print(county)
					for house_type in self.data[province][county]:
						item_list=self.data[province][county][house_type]
						desc_list=[]
						count=0
						for item in item_list:
							desc_list.append(item['description'])
							count+=1

						vect=TfidfVectorizer(min_df=1)
						if len(desc_list)>1:
							tfidf=vect.fit_transform(desc_list)
							matrix=(tfidf*tfidf.T).A
							query=[i for i in range(len(matrix))]
							del_list=[]
							while len(query)>1:
								index=query[0]
								for i in range(index+1,count):
									if matrix[index][i]>0.8 and item_list[i]['price']==item_list[index]['price'] and item_list[i]['area']==item_list[index]['area']:
										delta=datetime.datetime.strptime(str(item_list[index]['post-time']['date']),'%d-%m-%Y')-datetime.datetime.strptime(str(item_list[i]['post-time']['date']),'%d-%m-%Y')
										if delta.days<30:
											if i in query:
												json.dump(item_list[i],f,indent=4)
												json.dump(item_list[index],f,indent=4)
												f.write('\n===========================\n')

												query.remove(i)
												del_list.append(i)
								del query[0]
							del_list.sort(reverse=True)
							for i in del_list:
								del item_list[i]
						allcount+=len(item_list)
		print (allcount)



if __name__=='__main__':
	pdata=ProcessData()
	pdata.openFile()
