import scrapy
import re
import unicodedata
import datetime
import json
import os
from scrapy.selector import Selector

class AlonhadatSpider(scrapy.Spider):
	name = 'alonhadat'
	area = ''
	last_post_time = ''
	is_last_sell = ''
	is_last_rent = ''
	is_updated = ''
	next_url = ''
	def start_requests(self):		
		self.is_updated = False 
		self.is_last_sell = False
		self.is_last_rent = False
		urls = [
		'http://alonhadat.com.vn/nha-dat/can-ban.html',
		'http://alonhadat.com.vn/nha-dat/cho-thue.html'
		]

		for url in urls:
			yield scrapy.Request(url=url,callback=self.parse)
		

	def convert_unicode(self,text):
		if text=='':
			return text
		text=re.sub(unichr(272),'D',text);
		text=re.sub(unichr(273),'d',text);
		text=unicodedata.normalize('NFKD', text).encode('ascii','ignore')
		text=text.replace('\n','')
		text=text.replace('\t','')
		text=text.replace('\r','')
		return text

	def convert_price(self, price):
		list_price = price.split()
		if price.find('/') != -1:
			real_price = int(list_price[0]) * 1000000 * int(self.area)
			return real_price
		if list_price[1] == 'trieu':
			real_price = int(list_price[0]) * 1000000
		else:
			real_price = float(list_price[0].replace(",",".")) * 1000000000
		return real_price


	def parse(self, response):
		print(response.url)
		# Get all items
		items = response.xpath(".//div[@class= 'content-item']/div/div[@class='ct_title']/a/@href")
		self.next_url = response.url.rpartition("--")[0] + '--'
		if response.url.find('trang') == -1 and self.is_updated == False: # Process the first page
			print ("Process First Page")
			self.next_url = response.url.replace(".html","/trang--")
			self.is_updated = True
			print ("Start to open json file")
			with open('last_post_id.json','r+') as f:
				data=json.load(f)
				self.last_post_time=''
				if "alonhadat" in data:
					self.last_post_time = datetime.datetime.strptime(data["alonhadat"],"%d-%m-%Y %H:%M")
					data["alonhadat"] = (datetime.datetime.now()-datetime.timedelta(minutes=4)).strftime("%d-%m-%Y %H:%M")
			
			os.remove('last_post_id.json')
			with open('last_post_id.json','w') as f:
				json.dump(data,f,indent = 4)
		for item in items:
			print ("Process each item")
			print (item.extract())
			if(re.search('cho-thue', response.url)!=None):
				if self.is_last_rent == True:
					return
			else:
				if self.is_last_rent == True:
					return

			item_url = "http://alonhadat.com.vn" + item.extract()
			yield scrapy.Request(item_url,callback=self.parse_item)


		# Go to next page
		print("Next url 2: " + self.next_url)
		next_pages = response.xpath("//div[@class='page']/a[@rel='nofollow']/@href").extract()
		if len(next_pages) == 1:	# Ony one 'nofollow'
			next_pages = response.xpath("//div[@class='page']/a[@rel='nofollow']/@href").extract_first()
		else:	#  All pages are 'nofollow'
			next_pages = response.xpath("//div[@class='page']/a[@rel='nofollow']/@href")[len(next_pages)].extract()
		next_pages_index = int(next_pages.partition('--')[-1].rpartition('.html')[0])
		current_index = int(response.xpath("//a[@class='active']/text()").extract_first())
		if current_index < next_pages_index:
			current_index = current_index + 1
			next_page_url = self.next_url + str(current_index) + ".html"
			yield scrapy.Request(next_page_url,callback=self.parse)
		elif current_index == next_pages_index:
			next_page_url = self.next_url + str(next_pages_index) + ".html"
			yield scrapy.Request(next_page_url,callback=self.parse)

	def parse_item(self, response):
		# Get area
		self.area = response.xpath("//span[@class='square']/span[@class='value']/text()").extract_first()
		self.area = self.area.strip().replace(" m","")

		# Get price
		price = response.xpath("//span[@class='price']/span[@class='value']/text()").extract_first()
		price = self.convert_unicode(price)
		price = self.convert_price(price)
		# Get post id
		post_id = response.xpath(".//tr/td/text()")[1].extract()

		# Get property type
		property_type = self.convert_unicode(response.xpath(".//tr/td/text()")[13].extract())

		# Get transaction type
		transaction_type = self.convert_unicode(response.xpath(".//tr/td/text()")[7].extract())

		# Get post time
		post_date = response.xpath("//span[@class='date']/text()").extract_first()
		post_date = self.convert_unicode(post_date).replace('Ngay dang: ', '').replace("/","-")
		if post_date =="Hom nay":
			post_date=datetime.datetime.now()
		elif post_date == "Hom qua":
			post_date=datetime.datetime.now() - datetime.timedelta(1)
		else:
			post_date=datetime.datetime.strptime(post_date,"%d-%m-%Y") #
		weekday = post_date.weekday()
		print ("Post date:", post_date)
		print ("Last post time:", self.last_post_time)
		if post_date<self.last_post_time:
			print(post_date.strftime("%d-%m-%Y"),self.last_post_time.strftime("%d-%m-%Y"),response.url)
			if transaction_type=='Can ban':
				self.is_last_sell=True
			else:
				self.is_last_rent=True
			return
	
		# Get title
		title = self.convert_unicde(response.xpath('//div[@class="title"]/h1/text()').extract_first())

		# Get location
		location = response.xpath("//div[@class='add']/span[@class='value']/text()").extract_first()
		location = self.convert_unicode(location)

		# Get city (province)
		list_location = location.split(',')
		city = list_location[3]

		# Get district (ward)
		ward = list_location[2]

		# Get author name
		author = response.xpath("//span[@class='name']/span[@class='value']/text()").extract_first()

		# Get author phone
		phone = response.xpath("//span[@class='phone']/span[@class='value']/text()").extract_first()

		yield {
			'post-id': post_id,
			'website': "alonhadat.com.vn",
			'author': {'name': author , 'phone': phone},
			'post-time': {'date': post_date.strftime("%d-%m-%Y"),'weekday': weekday},
			'title': title,
			'location': {'city': city, 'ward': ward, 'detail': location},
			'area':area,
			'price':price,
			'transaction-type': transaction_type,
			'property-type': property_type
		}





