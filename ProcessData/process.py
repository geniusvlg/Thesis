import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import datetime
import copy


class ProcessData:

	path='./middle'
	data={}
	def openFile(self):
		for filename in os.listdir(self.path):
			print(filename)
			self.readFile(filename)
			self.data={}

	def readFile(self,filename):
		print("READ FILE")
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
				if container.get(item['house-type'])==None:
					container[item['house-type']]=[]
				container=container[item['house-type']]
				item["related"]=[]
				container.append(item)
			self.remove_duplication()
			self.printOutput(filename)

	def readStructure(self):
		print("READ FILE")
		for filename in os.listdir(self.path):
			print(filename)
			self.data={}
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
						container[item['location']['ward']]=[]
					container=container[item['location']['ward']]
					if item['house-type'] not in container:
						container.append(item['house-type'])

				self.printOutput(filename.split('.')[0]+'-STRUCT.t')


	def printOutput(self,filename):
		with open('./processed/'+filename[:-2]+'output.json','w') as f:
			json.dump(self.data,f,indent=4,separators=(',',': '),sort_keys=True)

	def remove_duplication(self):
		allcount=0
		remove_c=0
		with open('test.txt','w') as f:
			for t_type in self.data:
				by_type=self.data[t_type]
				for province in by_type:
					by_province=by_type[province]
					for county in by_province:
						print(county)
						by_county=by_province[county]
						for ward in by_county:
							if ward=='':
								continue
							by_ward=by_county[ward]
							for house_type in by_ward:
								desc_list=[]
								item_list=[]
								count=0
								for item in item_list:
									desc_list.append(item['description'])
									item_list.append(item)
									count+=1
								if "" in by_county:
									if house_type in by_county[""]:
										for item in by_county[""][house_type]:
											desc_list.append(item['description'])
											item_list.append(item)
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
												if delta.days<15:
													if i in query:
														json.dump(item_list[i],f,indent=4)
														json.dump(item_list[index],f,indent=4)
														f.write('\n===========================\n')
														del_list.append(i)
														query.remove(i)
														remove_c+=1
												else:
													if i in query:
														print(item_list[i]['post-id'])
														if item_list[i]['post-id'] not in item_list[index]['related']:
															item_list[index]['related'].append(item_list[i]['post-id'])
															item_list[i]['related'].append(item_list[index]['post-id'])
															query.remove(i)
												
										del query[0]
									del_list.sort(reverse=True)
									mi=len(by_ward[house_type])
									for i in del_list:
										if i <len(by_ward[house_type]):
											del by_ward[house_type][i]
										else:
											del by_county[""][house_type][i-mi]
								allcount+=len(item_list)
		print (allcount)
		print(remove_c)



if __name__=='__main__':
	pdata=ProcessData()
	command=input("What do you want: ?")
	if command=='struct':
		pdata.readStructure()
	elif command == 'process':
		pdata.openFile()
	