import os
import json
import datetime

def is_number(text):
		try:
			float(text)
			return True
		except ValueError:
			return False

def main(type):
	ret=[]
	if type=='raw':
		path='./data'
		for filename in os.listdir(path):
			years=[]
			count=[]
			nonpricecount=0
			nonareacount=0
			noboth=0
			total=0
			with open('./data/'+filename,'r') as f:
				for line in f:
					total+=1
					item= json.loads(line)
					date=datetime.datetime.strptime(item['post-time']['date'],'%d-%m-%Y')
					year=date.year
					noa=False
					nop=False
					if not is_number(str(item['area']).split('m')[0].replace(',','.')):
						nonareacount+=1
						noa=True
					if not is_number(str(item['price']).replace(',','.')):
						nonpricecount+=1
						nop=True
					if noa or nop:
						noboth+=1
					if year not in years:
						years.append(year)
						count.append(1)
					else:
						count[years.index(year)]+=1
			print("Year")
			print (filename)
			print(years)
			print("No area: {}, no price: {}, no both: {}".format(nonareacount,nonpricecount,noboth))
			print("Good portion {}%".format((total-noboth)/total*100))
			ret.append(total)
	elif type=='process':
		path='./processed'
		for filename in os.listdir(path):
			with open(path+'/'+filename,'r') as f:
				years=[]
				count=[]
				nonpricecount=0
				nonareacount=0
				noboth=0
				data=json.load(f)
				total=0
				for province in data:
					by_province=data[province]
					for county in by_province:
						by_county=by_province[county]
						for ward in by_county:
							by_ward=by_county[ward]
							for road in by_ward:
								by_road=by_ward[road]
								for house_type in by_county:
									by_house=by_county[house_type]
									for item in by_house:
										total+=1
										date=datetime.datetime.strptime(item['post-time']['date'],'%d-%m-%Y')
										year=date.year
										noa=False
										nop=False
										if not is_number(str(item['area']).split('m')[0].replace(',','.')):
											nonareacount+=1
											noa=True
										if not is_number(str(item['price']).replace(',','.')):
											nonpricecount+=1
											nop=True
										if noa or nop:
											noboth+=1
										if year not in years:

											years.append(year)
											count.append(1)
										else:
											count[years.index(year)]+=1
				print("Year")
				print (filename)
				print(years)
				print(count)
				print("No area: {}, no price: {}, no both: {}".format(nonareacount,nonpricecount,noboth))
				print("Good portion {}%".format((total-noboth)/total*100))
				ret.append(total-noboth)
	return ret



if __name__ == '__main__':
	remain=main('process')
	total=main('raw')
	for i in range(len(total)):
		print("Last level: {}%".format(remain[i]/total[i]*100))