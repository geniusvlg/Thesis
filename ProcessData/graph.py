import json


def is_number(text):
		try:
			float(text)
			return True
		except ValueError:
			return False

class stats:
	stats={}

	def main(self):
		with open('./batdongsan.output.json') as f:
			storage=json.load(f)
			for province in storage:

				if province not in self.stats:
					self.stats[province]={}
				tprice2 = 0
				count2=0
				for county in storage[province]:
					if county not in self.stats[province]:
						self.stats[province][county]={}
					tprice1=0
					count1=0
					for house_type in storage[province][county]:
						tprice0=0
						count0=0
						for item in storage[province][county][house_type]:
							if is_number(str(item['price'])):
								if 'Khong xac dinh' not in item['area']:
									area=item['area'].split('m')
									if is_number(area[0]) and float(area[0])>0:
										tprice0+=item['price']/float(area[0])
										count0+=1
						if count0>0:
							self.stats[province][county][house_type]=float(tprice0/count0)
							tprice1+=float(tprice0/count0)
							count1+=1
						else:
							self.stats[province][county][house_type]=0
						
					if count1>0:
						self.stats[province][county]['avg']=float(tprice1/count1)
						tprice2+=float(tprice1/count1)
						count2+=1
					else:
						self.stats[province][county]['avg']=0
					
				if count2>0:
					self.stats[province]['avg']=float(tprice2/count2)
				else:
					self.stats[province]['avg']=0
		with open('stats.txt','w') as of:
			json.dump(self.stats,of,indent=4,separators=(',',': '),sort_keys=True)


if __name__ == '__main__':
	stat= stats()
	stat.main()