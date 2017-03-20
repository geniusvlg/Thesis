import scrapy
import re
import unicodedata
import datetime
import json
import os
from scrapy.selector import Selector

class NhadatVnSpider(scrapy.Spider):
	name = "Nhadatvn"
	last_post_time=''
	is_last=''
	def start_requests(self):
		global is_last
		is_last=False
		urls = [
		'https://raovat.nhadat.vn/cho-thue-4/?prefixid=0&prefixid2=0&direction=0&price=0',
		'https://raovat.nhadat.vn/can-ban-12/?prefixid=0&prefixid2=0&direction=0&price=0'
		]
		for url in urls:
			yield scrapy.Request(url=url,callback=self.parse)
	

	def convert_unicode(self,text):
		return unicodedata.normalize('NFKD', text).encode('ascii','ignore')

	def convert_price(self,text):
		if(bool(re.search(r'\d',text))==False):
			return text
		else :
			#get the base number, and the unit (Ngan, Trieu, Ty)
			price_s=text.split(' ')
			real_price=0

			base=float(price_s[0].replace(',','.'))
			unit=price_s[1]
			if unit[0]=='N':
				real_price+=(base)*1000
			elif unit[0]=='T':
				if unit[1]=='r':
					real_price+=(base)*1000000
				else:
					real_price+=(base)*1000000000
			return real_price

	def parse_item(self,response):
		#get basic info of property
		property_info = response.xpath(".//div[contains(@class,'uifleft')]/dl/dd/text()").extract()
		#get author info
		author_info = response.xpath(".//div[contains(@class,'uifright')]/dl/dd/text()").extract()
		#get description
		item_content = self.convert_unicode(re.sub("\r|\n|\t",""," ".join(response.xpath(".//blockquote/text()").extract())))

		#get title
		title=self.convert_unicode(response.xpath(".//span[contains(@class,'threadtitle')]/a/text()").extract_first())

		breadcrumb=response.xpath(".//span[contains(@class,'crust')]")
		#Rent or sell
		transaction_type = self.convert_unicode(breadcrumb[1].xpath("./a/span/text()").extract_first())
		#Basic house type
		general_house_type = self.convert_unicode(breadcrumb[2].xpath("./a/span/text()").extract_first())
		#Detailed house type
		housetype=self.convert_unicode(breadcrumb[3].xpath("./a/span/text()").extract_first())

		date=self.convert_unicode(response.xpath(".//span[contains(@class,'postdate')]/span/text()").extract_first()).strip(" ")
		if date =="Hom nay":
			date=datetime.datetime.now()
		elif date == "Hom qua":
			date=datetime.datetime.now() - datetime.timedelta(1)
		else:
			date=datetime.datetime.strptime(date,"%d-%m-%Y")
		global is_last
		global is_first
		weekday=date.weekday()
		if date<last_post_time:
			print(date,last_post_time)
			is_last=True
		county = self.convert_unicode(property_info[1])
		province = self.convert_unicode(property_info[0])
		if re.search("HCM",province)!=None:
			provice="HCM"
		area=""
		price=None
		if len(property_info)>3:
			area = property_info[2]
			price=self.convert_unicode(property_info[3])
			area=area.split(" ")[0]
		elif len(property_info)==3:
			area= None
			price= self.convert_unicode(property_info[2])
			
		price=self.convert_price(price)

		post_id = author_info[0]
		author=response.xpath(".//div[contains(@class,'uifright')]/dl/dd")[1].xpath("./div/a/@title").extract_first()
		author=author.split(" ")[0]
		phone=None

		if len(author_info)==2:
			phone=author_info[1]

		yield {
			'post-id': post_id,
			'website': "nhadat.vn",
			'author': author,
			'post-time': {'date': date.strftime("%d-%m-%Y"),'weekday': weekday},
			'title': title,
			'location': {'county': county,'province': province,'location-detail':''},
			'area':area,
			'price':price,
			'transaction-type': transaction_type,
			'house-type': {'general':general_house_type,'detailed':housetype},
			'description': item_content
		}

	def parse(self, response):
		#get all item 
		items=response.xpath("//li[contains(@class,'threadbit')]")

		if response.url.find('index')==-1: #first page
			global last_post_time
			with open('last_post_id.json','r+') as f:
				data=json.load(f)
				if "Nhadatvn" in data:
					last_post_time=datetime.datetime.strptime(data["Nhadatvn"],"%d-%m-%Y %H:%M")
					data["Nhadatvn"]=(datetime.datetime.now()-datetime.timedelta(minutes=15)).strftime("%d-%m-%Y %H:%M")
			os.remove('last_post_id.json')
			with open('last_post_id.json','w') as f:
				json.dump(data,f,indent = 4)

		for item in items:
			if is_last==True:
				break
			item_id = item.xpath(".//a[contains(@class,'title')]/@id").extract_first().split('_')[2]
			item_url = item.xpath(".//h2[contains(@class,'threadtitle')]/a/@href").extract_first()
			yield scrapy.Request(item_url,callback=self.parse_item)

		#if there is no expired item, go to next page, if there is a next page
		if is_last==False:
			next_href=response.xpath("//a[contains(@rel,'next')]/@href")
			next_href_address=response.xpath("//a[contains(@rel,'next')]/@href").extract_first()
			if next_href!=[]:
				yield scrapy.Request(next_href_address,callback=self.parse)
