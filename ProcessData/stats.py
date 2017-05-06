import os
import json
import datetime

def is_number(self,text):
		try:
			float(s)
			return True
		except ValueError:
			return False

def main():
	path='./data'
	for filename in os.listdir(path):
		years=[]
		count=[]
		nonpricecount=0
		nonareacount=0
		with open('./data/'+filename,'r') as f:
			for line in f:
				item= json.loads(line)
				date=datetime.datetime.strptime(item['post-time']['date'],'%d-%m-%Y')
				year=date.year
				if is_number(str(item['area'])):
					print (item['area'])
					nonareacount+=1
				if is_number(str(item['price'])):
					nonpricecount+=1
					print(item['price'])
				if year not in years:

					years.append(year)
					count.append(1)
				else:
					count[years.index(year)]+=1
		print("Year")
		print(years)
		print(count)
		print(nonareacount,nonpricecount)

if __name__ == '__main__':
	main()