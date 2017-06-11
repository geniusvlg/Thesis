import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import datetime
import copy
import math
import numpy as np


def is_number(text):
    try:
        float(text)
        return True
    except ValueError:
        return False

class ProcessData:

<<<<<<< Updated upstream
    path='./middle'
    data={}

    def process(self):
        self.open_file()
        self.remove_duplication()
        self.remove_by_modified_z_score()
        self.print_output()

    def open_file(self):
        for filename in os.listdir(self.path):
            print(filename)
            self.read_file(filename)

    def read_file(self,filename):
        print("READ FILE")
        with open(self.path+'/'+filename,'r') as f:
            ite=0
            for line in f:
                if ite%500==0:
                    print('Processing item {}'.format(ite+1))
                ite+=1
                item=json.loads(line)
                valid = False
                if(is_number(str(item['area']).split('m')[0].replace(',','.')) and is_number(str(item['price']).replace(',','.'))):
                    if int(float(item['area'].split('m')[0].replace(',','.')))!=0 and item['price']!= 0:
                        item['price']=int(float(str(item['price']).replace(',','.'))/float(item['area'].split('m')[0].replace(',','.')))
                        item['area']=float(item['area'].split('m')[0].replace(',','.'))
                        valid = True

                if valid == False:
                    continue

                if self.data.get(item['transaction-type'])==None:
                    self.data[item['transaction-type']]={}
                container=self.data[item['transaction-type']]
                if container.get(item['location']['province'])==None:
                    container[item['location']['province']]={}
                container=container[item['location']['province']]
                if container.get(item['location']['county'])==None:
                    container[item['location']['county']]={}
                container=container[item['location']['county']]
                # if container.get(item['location']['ward'])==None:
                #     container[item['location']['ward']]={}

                # container=container[item['location']['ward']]
                if container.get(item['house-type'])==None:
                    container[item['house-type']]=[]
                container=container[item['house-type']]
                item["related"]=[]
                
                container.append(item)

    def read_structure(self):
        print("READ FILE")
        for filename in os.listdir(self.path):
            print(filename)
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

        with open('./processed/output.json','w') as f:
            json.dump(self.data,f,indent=4,separators=(',',': '),sort_keys=True)

    def read_structure_json(self):
        with open('./processed/merge_output.json','r') as f:
            data=json.load(f)
            for t_type in data:
                by_type=data[t_type]
                for province in by_type:
                    by_province=by_type[province]
                    for county in by_province:
                        print(county)
                        by_county=by_province[county]
                        for ward in by_county:
                            by_county[ward]=[]
            with open('./processed/struct.json','w') as fo:
                json.dump(data,fo,indent=4,separators=(',',': '),sort_keys=True)

    def remove_by_iqr(self):
        count=0
        total=0
        for t_type in self.data:
            by_type=self.data[t_type]
            for province in by_type:
                by_province=by_type[province]
                for county in by_province:
                    
                    by_county=by_province[county]
                    print(county)
                    #for ward in by_county:
                        # if ward=='':
                        #     continue
                        #by_ward=by_county[ward]
                    for house_type in by_county:
                        total+=1
                        array=[int(x['price']) for x in by_county[house_type]]
                        array.sort()
                        q1 = self.get_quartile(array,0)
                        q3 = self.get_quartile(array,1)
                        iqr=q3-q1
                        if iqr==0:
                            count+=1
                        del_list=[]
                        if iqr!=0:
                            for i in range(len(by_county[house_type])):
                                item=by_county[house_type][i]
                                if (int(item['price']) > (q3 + 3 * iqr) or int(item['price']) < (q1 - 3 * iqr)):
                                    del_list.append(i)
                            del_list.sort(reverse=True)
                            for i in del_list:
                                del by_county[house_type][i]
        print("IQR = 0 {} in {}".format(count,total))

    def get_quartile(self,array,rank):
        half_length = int(len(array)//2)
        if (half_length%2==0):
            return ((array[int(half_length/2 - 1 + half_length * rank)]) + (array[int(half_length / 2 + half_length * rank)]))/2
        else:
            return int(array[(half_length//2 + half_length * rank)])

    def print_output(self):
        with open('./processed/merge_output.json','w') as f:
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
                        # for ward in by_county:
                        #     if ward=='':
                        #         continue
                        #     by_ward=by_county[ward]
                        for house_type in by_county:
                            desc_list=[]
                            item_list=[]
                            count=0
                            for item in by_county[house_type]:
                                desc_list.append(item['description'])
                                item_list.append(item)
                                count+=1
                            if "" in by_province:
                                if house_type in by_province[""]:
                                    for item in by_province[""][house_type]:
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
                                mi=len(by_county[house_type])
                                for i in del_list:
                                    if i <len(by_county[house_type]):
                                        del by_county[house_type][i]
                                    else:
                                        del by_county[""][house_type][i-mi]
                            allcount+=len(item_list)
        print(remove_c)

    def remove_by_modified_z_score(self):
        count=0
        total=0
        of = open('remove_mzs.txt','w')
        for t_type in self.data:
            by_type=self.data[t_type]
            for province in by_type:
                by_province=by_type[province]
                for county in by_province:
                    
                    by_county=by_province[county]
                    print(county)
                    #for ward in by_county:
                        # if ward=='':
                        #     continue
                        #by_ward=by_county[ward]
                    
                    for house_type in by_county:
                        del_list=[]
                        total+=1
                        array=[int(x['price']) for x in by_county[house_type]]
                        median = np.median(array)
                        median_absolute_deviation = np.median([np.abs(x - median) for x in array]) 
                        if median_absolute_deviation==0:
                            continue
                        for i, item in enumerate(by_county[house_type]):
                            if np.abs(0.6745*(item['price']-median)/median_absolute_deviation)>5:
                                del_list.append(i)
                        del_list.sort(reverse=True)
                        for i in del_list:
                            area=float(item['area'])
                            of.write(str(by_county[house_type][i]['price'])+" "+str(by_county[house_type][i]['price']*area)+" "+ str(by_county[house_type][i]['price'])+" "+by_county[house_type][i]['house-type']+ " "+ by_county[house_type][i]['transaction-type']+" "+ str(median) + " "+ str(median_absolute_deviation)+'\n')
                            del by_county[house_type][i]
        of.close()

    def remove_by_std(self):
        count=0
        for t_type in self.data:
            by_type=self.data[t_type]
            for province in by_type:
                by_province=by_type[province]
                for county in by_province:
                    print(county)
                    by_county=by_province[county]
                    for ward in by_county:
                        # if ward=='':
                        #     continue
                        by_ward=by_county[ward]
                        for house_type in by_ward:
                            mean = self.calMean(by_ward[house_type])
                            standard = self.calStd(by_ward[house_type], mean)
                            if ward=='phuong 22':
                                print("MEAN STANDARD {} {}".format(mean,standard))
                            for item in by_ward[house_type]:
                                if int(item.get("price")) < (mean - 3*standard) or int(item.get("price")) > (mean + 3*standard):
                                    by_ward[house_type].remove(item)
                                    count+=1
        print("Remove by STD {}".format(count))

    def calMean(self,list):
        total = 0
        for item in list:
            if(isinstance(item.get("price"),str)):
                print(item.get("price"))
=======
	path='./data'
	data={}
	def openFile(self):
		for filename in os.listdir(self.path):
			print(filename)
			self.data={}

	def readFile(self,filename):
		print("READ FILE")
		with open(self.path+'/'+filename,'r') as f:
			ite=0
			for line in f:
				print ("line")
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
			json.loads(self.data,f,indent=4,separators=(',',': '),sort_keys=True)

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
>>>>>>> Stashed changes

            total += int(item.get("price"))
        return total / len(list)

    def calStd(self, list, mean):
        if len(list) == 1:
            return 0
        total = 0
        variance = 0
        for item in list:
            variance  = variance + math.pow((int(item.get("price")) - mean),2)
        variance = variance / len(list)
        return math.sqrt(variance)

if __name__=='__main__':
    pdata=ProcessData()
    command=input("What do you want: ?")
    if command=='struct':
        pdata.read_structure()
    elif command == 'process':
        pdata.process()
    elif command == 'structjson':
        pdata.read_structure_json()
    