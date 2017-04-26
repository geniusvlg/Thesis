import scrapy
import re
import unicodedata
import datetime
import json
import os
from scrapy.selector import Selector
from scrapy_splash import SplashRequest

class QuotesSpider(scrapy.Spider):
	name = "diaoconline"
	last_post_time=''
	is_last_sell=''
	is_last_rent=''
	is_updated=''

	def start_requests(self):
		global is_last
		is_last=False
		urls = [
		'http://alonhadat.com.vn/nha-dat/can-ban.html'
		]
		for url in urls:
			yield SplashRequest(url, self.parse, endpoint='render.html',args={'wait': 0.5},)

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

	def convert_price(self,price):
		list_price = price.split()
		if len(price) > 3:
			real_price = float(list_price[0])*1000000000 + float(list_price[2])*1000000
		else:
			if 'trieu' in price:
				real_price = float(list_price[0])*1000000
			else:
				real_price = float(list_price[0])*1000000000
		return real_price

	def parse(self, response, index):

		# Get all posts
		items = response.xpath(".//div[contains(@class, rounded_style_2)]")

		# Process the first page
		if response.url() == -1:
			global last_post_time
			with open('last_post_id.json', 'r+') as f:
				data=json.load(f)
				if "diaoconline" in data:
					last_post_time=datetime.datetime.strptime(data["diaoconline"],"%d-%m-%Y %H:%M")
					data["diaoconline"]=(datetime.datetime.now()-datetime.timedelta(minutes=15)).strftime("%d-%m-%Y %H:%M")
			os.remove('last_post_id.json')
			with open('last_post_id.json','w') as f:
				json.dump(data,f,indent = 4)
					
		for item in items:
			post_time = self.convert_unicode(item.xpath("//span[@class='post_type']/text()").extract_first())
			if('truoc' in post_time):
				date=datetime.datetime.now()
			else:
				date=datetime.datetime.strptime(date,"%d-%m-%Y")
			if date < last_post_time:
				print(date,last_post_time)
				return
			
			# Get URL of each item
			item_url = item.xpath(".//div[contains(@class, 'info margin_left')]/h2/a/@href").extract_first()
			item_url =  "http://diaoconline.vn" + item_url
			yield scrapy.Request(item_url,callback=self.parse_item)

		# Go to next page
		next_href = response.xpath("//a[contains(@rel, 'next')]/@href").extract_first()
		if next_href == None:
			next_href = "http://http://diaoconline.vn" + next_href;
			yield SplashRequest(next_href, self.parse, endpoint='render.html',args={'wait': 0.5},)

	def	parse_item(self, response):
		# Get price of property
		price = response.xpath("//div[contains(@class, 'money')]/text()").extract_first()
		price = price.strip()
		price = self.convert_unicode(price)
		if ('luong' in price):
			return 

		price = self.convert_price(re.sub('Gia:','',price))

		# Get description of property
		description = self.convert_unicode(response.xpath('//div[contains(@class,"body")]/p/text()').extract_first())

		# Get Title
		title = self.convert_unicode(response.xpath('//h1[contains(@class, "larger_title")]/text()').extract_first())

		# Get Post ID
		post_id = response.xpath("//div[contains(@class, 'feat_item')]/dl/dd").extract_first()

		# Get Area
		area = re.sub('[\r\n]', '', self.convert_unicode(response.xpath("//div[@class='feat_item']/dl/dd/text()")[1].extract()))

		# Get author name
		author_name = self.convert_unicode(response.xpath('//div[contains(@class, "body")]/h4/a/text()').extract_first())

		# Get author phone number
		author_phone = response.xpath("//div[@class='body']/dl/dd/span/text()").extract_first()

		# Get location of property
		location = re.sub('Vi tri:\r\n','',self.convert_unicode(response.xpath('//span[contains(@class, "location")]/text()').extract_first()))

		# Get provience
		location_array = location.split(',')
		province = location_array[3]

		# Get county
		county = location_array[2]
		
		# Get house type
		house_type = self.convert_unicode(response.xpath("//strong/a[@class='link-ext']/text()").extract_first())

		# Get transaction type
		transaction_type = self.convert_unicode(response.xpath("//span[@itemprop='title']/text()")[1].extract())
		
		yield {
			'post-id': post_id
		} 

		