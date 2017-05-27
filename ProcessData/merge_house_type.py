import json
import os

class Fix():
	path='./data'
	def merge_house_type(self):
		with open("house_type_conversion.json",'r') as f:
			self.convert_table=json.load(f)
		for filename in os.listdir(self.path):
			with open('./middle/'+filename,'w') as fo:
				with open(self.path+'/'+filename,'r') as f:
					ite=0
					for line in f:
						ite+=1
						if ite%5000==0:
							print("Processed {}".format(ite))
						item=json.loads(line)
						try:
							merged_type=self.convert_table[item['website']][item['house-type']]
							item['house-type']=merged_type
							json.dump(item,fo)
							fo.write("\n");
						except Exception:
							print(item)
						



if __name__=='__main__':
	main=Fix()
	main.merge_house_type()
