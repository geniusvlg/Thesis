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
				if self.data.get(item['transaction-type'])==None:
					self.data[item['transaction-type']]={}
				container=self.data[item['transaction-type']]
				if container.get(item['location']['province'])==None:
					container[item['location']['province']]={}
				container=container[item['location']['province']]
				if container.get(item['location']['county'])==None:
					container[item['location']['county']]={}
				container=container[item['location']['county']]
				if container.get(item['location']['ward'])==None:
					container[item['location']['ward']]={}
				container=container[item['location']['ward']]
				if container.get(item['location']['road'])==None:
					container[item['location']['road']]={}
				container=container[item['location']['road']]
				if container.get(item['house-type'])==None:
					container[item['house-type']]=[]
				container=container[item['house-type']]

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
			for t_type in self.data:
				by_type=self.data[t_type]
				for province in by_type:
					by_province=by_type[province]
					for county in by_province:
						print(county)
						by_county=by_province[county]
						for ward in by_county:
								by_ward=by_county[ward]
								for road in by_ward:
									by_road=by_ward[road]
									for house_type in by_road:
										item_list=by_road[house_type]
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
