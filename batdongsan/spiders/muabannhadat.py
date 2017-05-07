import scrapy
import re
import unicodedata
import datetime
import json
import os
from scrapy.selector import Selector

class MuabannhadatSpider(scrapy.Spider):
	name = "muabannhadat"
	last_post_time=''
	is_last_rent = ''
	is_last_sell = ''
	is_updated = ''
	transaction_type = ''

	def start_requests(self):
		self.is_last_rent=False
		self.is_last_sell=False
		self.is_updated=False
		urls = [
		'http://www.muabannhadat.vn/nha-ban-3513',
		'http://www.muabannhadat.vn/nha-cho-thue-3518'
		]
		for url in urls:
			yield scrapy.Request(url=url,callback=self.parse)

	def convert_unicode(self,text):
		if text=='':
			return text
		text=re.sub(chr(272),'D',text);
		text=re.sub(chr(273),'d',text);
		text=unicodedata.normalize('NFKD', text).encode('ascii','ignore')
		text=text.decode()
		text=text.replace('\n','')
		text=text.replace('\t','')
		text=text.replace('\r','')
		return text

	def convert_price(self, item_price):
		item_price = self.convert_unicode(item_price)
		price_number = price.split(" ")[0]
		price_unit = price.split(" ")[1]
		price_number = re.sub(",",".",price_number)
		if price_unit[1] == "r":
			return  (float(price_number)*1000000)
		elif price_unit[1] == "y":
			return (float(price_number)*1000000000)

	def parse(self, response):  
		# Get all items from the page
		items = response.xpath("//div[contains(@class, 'list-group-item')]")

		# We use is_updated here because we want the first page to be run only one time for both 2 links
		if (response.url.find("p=")==-1) and self.is_updated==False: # Process the first page
			self.is_updated = True
			with open('last_post_id.json', 'r+') as f:
				data = json.load(f)
				if "muabannhadat" in data:
					self.last_post_time=datetime.datetime.strptime(data["muabannhadat"],"%d-%m-%Y %H:%M")
					data["muabannhadat"]=(datetime.datetime.now()-datetime.timedelta(minutes=4)).strftime("%d-%m-%Y %H:%M")		
			
			os.remove('last_post_id.json')
			with open('last_post_id.json', 'w') as f:
				json.dump(data, f, indet = 4)

		# Read every post one by one
		for item in items:
			if (re.search('cho-thue', response.url) != None):
				self.transaction_type = 'cho thue'
				if self.is_last_rent == True:
					return
			else:
				self.transaction_type = 'nha ban'
				if self.is_last_sell == True:
					return
			item_url = item.xpath("//a[@class='title-filter-link']/@href").extract_first()
			yield scrapy.Request(item_url,callback=self.parse_item)

		# Go to the next page
		next_page = response.xpath("//a[contains(@id,'_lnkNext')]/@href")
		if next_page != []:
			next_page = response.xpath("//a[contains(@id,'_lnkNext')]/@href").extract_first()
			next_page_address = "http://www.muabannhadat.vn" + next_page
			yield scrapy.Request(next_page_address,callback=self.parse)

	def parse_item(self, response):

		# Get description of the property
		post_desciption = self.convert_unicode(re.sub("\r|\n|\t",""," ".join(response.xpath(".//div[contains(@id, 'Description')]/text()").extract()))).strip(" ")

		# Get the price
		post_price = self.convert_price(response.xpath('//span[contains(@class,"price")]/text()').extract_first())

		# Get the area
		area = self.convert_unicode(response.xpath("//span[contains(@id,'_lblSurface')]/text()").extract_first()).replace(" m2","")
		
		# Get the post id
		post_id = response.url.rsplit('-',1)[1]

		# Get the post title
		post_title = self.convert_unicode(response.xpath("//h1[contains(@class, 'navi-title')]//text()").extract_first()).strip()

		# Get date post
		date_post =  self.convert_unicode(response.xpath("//span[contains(@id,'DateCreated')]/text()").extract_first()).replace(".","-")

		date_post = datetime.datetime.strptime(date_post,"%d-%m-%Y")
		weekday = date_post.weekday()
		if date_post < self.last_post_time:
			if self.transaction_type == 'cho thue':
				self.is_last_rent = True
			else:
				self.is_last_sell = True
			return

		# Get updated post
		date_update = self.convert_unicode(response.xpath("//span[contains(@class,'date-update')]/text()").extract_first()).replace(".","-")

		# Get city 
		city = self.convert_unicode(response.xpath("//span[contains(@id,'City')]/a/text()").extract_first())
		
		# Get district 
		district = self.convert_unicode(response.xpath("//span[contains(@id,'District')]/a/text()").extract_first())

		# Get ward
		ward = self.convert_unicode(response.xpath("//span[contains(@id,'Ward')]/a/text()").extract_first())

		# Get author
		author = re.sub("[Ms |Mr ]","",self.convert_unicode(response.xpath("//span[contains(@id, 'ContactName')]/text()").extract_first()))

		yield {
			'post-id': post_id,
			'website': "muabannhadat.vn",
			'author': author,
			'post-time': {'date': date.strftime("%d-%m-%Y"),'weekday': weekday},
			'title': post_title,
			'location': {'city': city,'district': district, 'ward':ward},
			'area':post_area,
			'price':post_price,
			'transaction-type': self.transaction_type,
			'description': post_desciption
		}