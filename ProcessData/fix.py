import json
import os

class Fix():
	def openFile(self):
		with open('batdongsan.jl','r') as f:
			with open('batdongsan1.jl','w') as fo:
				ite=0
				for line in f:
					item=json.loads(line)
					house_type_text=item['house-type']['detailed']
					pos=house_type_text.find('tai')
					item['house-type']['detailed']=house_type_text[:pos]
					json.dump(item,fo,encoding='ascii')
					ite+=1
					if(ite%500==0):
						print("Process {}".format(ite+1))

if __name__=='__main__':
	main=Fix()
	main.openFile()
