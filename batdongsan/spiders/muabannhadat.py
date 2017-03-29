import scrapy
import re
import unicodedata
import datetime
import json
import os
from scrapy.selector import Selector

class MuaBanNhaDatSpider(scrapy.Spider):
	name = "muabannhadat"
	last_post_time=''
	urls = ["http://www.muabannhadat.vn/nha-ban-3513"]

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
		is_last = False    
		# Get all items from the page
		items = response.xpath("//div[contains(@class, 'list-group-item')]")

		# Process the first page
		if (response.url.find("p=")==-1) or (response.url.find("p=0")!= -1):
			with open('last_post_id.json', 'r+') as f:
				data = json.load(f)
				if "Muabannhadat" in data:
					last_post_time=datetime.datetime.strptime(data["Nhadatvn"],"%d-%m-%Y %H:%M")
					data["Nhadatvn"]=(datetime.datetime.now()-datetime.timedelta(minutes=4)).strftime("%d-%m-%Y %H:%M")
				
			os.remove('last_post_id.json')
			with open('last_post_id.json', 'w') as f:
				json.dump(data, f, indet = 4)

		# Read every post one by one
		for item in items:
			item_url = item.xpath("//a[@class='title-filter-link']/@href").extract_first()
			yield scrapy.Request(item_url,callback=self.parse_item)

		# Go to the next page
		next_page = response.xpath("//a[contains(@id,'_lnkNext')]/@href").extract_first()
		if next_page != []:
			next_page_address = "http://www.muabannhadat.vn" + next_page
			yield scrapy.Request(next_page_address,callback=self.parse)

	def parse_item(self, response):
		# Get description of the property
		post_desciption = self.convert_unicode(re.sub("\r|\n|\t",""," ".join(response.xpath(".//div[contains(@id, 'Description')]/text()").extract())))

		# Get the price
		post_price = self.convert_price(response.xpath('//span[contains(@class,"price")]/text()').extract_first())

		# Get the area
		post_area = self.convert_unicode(response.xpath("//span[contains(@id,'_lblSurface')]/text()").extract_first())
		
		# Get the post id
		post_id = response.url.rsplit('-',1)[1]

		# Get the post title
		post_title = response.xpath("//h1[contains(@class, 'navi-title')]//text()").extract_first()

		

		yield {
			'post-id': post_id,
			'website': "muabannhadat.vn",
			#'author': author,
			#'post-time': {'date': date.strftime("%d-%m-%Y"),'weekday': weekday},
			'title': post_title,
			#'location': {'county': county,'province': province},
			'area':post_area,
			'price':post_price,
			'transaction-type': transaction_type,
			'house-type': {'general':general_house_type,'detailed':housetype},
			'description': post_desciption
		}