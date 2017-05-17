import json
import itertools
import os
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt



def is_number(text):
		try:
			float(text)
			return True
		except ValueError:
			return False

def draw_histo(array):
	plt.hist(array,bins=range(0,1000,10))
	plt.title("Count in leaf node")
	plt.xlabel("Count")
	plt.ylabel("Frequency")

	fig = plt.gcf()
	plt.show()


def comp(item):
	return int(item[1])


class stats:
	stats={}
	count=[]
	barecount=[]
	path='./processed'
	statpath='./stat'
	def main(self):

		for name in os.listdir(self.path):
			with open(self.path+'/'+name) as f:
				storage=json.load(f)
				self.dict_mean(storage,self.stats)
			with open(self.statpath+'/'+name.split('.')[0]+'stats.txt','w') as of:
				json.dump(self.stats,of,indent=4,separators=(',',': '),sort_keys=True)

	def dict_mean(self,value,container):
		total=0
		for k,v in value.items():
			val=0
			if isinstance(v,dict):
				key=k
				if k=='':
					key='Other'
				container[key]={}
				val=self.dict_mean(v,container[key])
			else:
				total_price=0
				for item in v:
					if is_number(item['price']):
						total_price+=item['price']
				val=container[k]=total_price/len(v)
			total+=val
		container['mean']=total/len(value)
		return total


	def dict_print(self,value,before):
		for k,v in value.items():
			if isinstance(v,dict):
				self.dict_print(v,k+', '+before)
			else:
				self.count.append((k+', '+before,len(v)))
				self.barecount.append(len(v))
	def get_leaf(self):
		
		for name in os.listdir(self.path):
			with open(self.path+'/'+name) as f:
				storage=json.load(f)
				self.dict_print(storage,'')
				self.count=sorted(self.count,key=lambda k: k[1],reverse=True)
				with open(self.statpath+'/count'+name.split('.')[0]+'.txt','w') as of:
					json.dump(self.count,of,indent=4,separators=(',',': '),sort_keys=True)
				with open(self.statpath+'/bcount'+name.split('.')[0]+'.txt','w') as of:
					json.dump(self.barecount,of,indent=4,separators=(',',': '),sort_keys=True)
				draw_histo(self.barecount)





if __name__ == '__main__':
	stat= stats()
	# stat.get_leaf()
	stat.main()