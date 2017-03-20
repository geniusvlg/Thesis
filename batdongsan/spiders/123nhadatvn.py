import scrapy
import re
import unicodedata
import datetime
import json
import os
from scrapy.selector import Selector

class Nhadat123Spider(scrapy.Spider):
	name="123nhadat"
	last_post_time=''
	cur_page_index=2
	start_urls=[
		"http://123nhadat.vn/raovat-c2/nha-dat-cho-thue",
		"http://123nhadat.vn/raovat-c1/nha-dat-ban"
	]
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

	def convert_time(self,text,item):
		post_time=None
		if re.search("/",text):
			post_date_text=self.convert_unicode(item.xpath("./div/div/div/ul/li/span/span/text()").extract_first().split(" ")[2])
			post_time=datetime.datetime.strptime(post_date_text,"%d/%m/%Y")
		elif re.search("phut|gio",text)!=None and re.search("ngay",text)==None:
			post_time=datetime.datetime.now()
		elif re.search("ngay",text)!=None:
			hours=0
			if re.search("gio",text)!=None:
				hours=int(self.convert_unicode(item.xpath("./div/div/div/ul/li/span/span/text()").extract_first().split(" ")[2]))
			days=int(self.convert_unicode(item.xpath("./div/div/div/ul/li/span/span/text()").extract_first().split(" ")[0]))
			post_time=datetime.datetime.now()-datetime.timedelta(days=days,hours=hours)
		elif re.search("moi cap nhat",text)!=None:
			post_time=datetime.datetime.now()
		return post_time
	def parse_item(self,response):
		title= self.convert_unicode(response.xpath(".//h1[@class='tieude_nhadat']/text()").extract_first())

		url_title= self.convert_unicode(response.xpath(".//ul[@class='info_no2']/li/span/a/text()").extract_first())
		house_type="";
		transaction_type=""
		if(re.search("Cho thue",url_title)!= None):
			house_type=url_title[url_title.find("Cho thue")+9:url_title.find("tai")-1]
			transaction_type="Cho thue"
		elif re.search("Ban",url_title!= None):
			house_type=url_title[url_title.find("Ban")+4:url_title.find("tai")-1]
			transaction_type="Can ban"

		details=response.xpath(".//div[@class='detail_khungxam']")

		description=self.convert_unicode(" ".join(details[0].xpath("./p//text()").extract()))

		post_id= response.url.split('/')[3].split('-')[1][1:]

		raw_last_update_time=details[1].xpath("./div")[2].xpath("./text()").extract_first().split(" ")
		last_update_time=self.convert_unicode(raw_last_update_time[len(raw_last_update_time)-2]+" "+raw_last_update_time[len(raw_last_update_time)-1])
		last_update_time=datetime.datetime.strptime(last_update_time,"%H:%M %d/%m/%Y")

		author=self.convert_unicode(response.xpath(".//div[@class='lienhe_nguoiban']/ul/li")[1].xpath("./b/text()").extract_first())

		location=self.convert_unicode(response.xpath(".//ul[@class='info_no2']/li/span/text()").extract_first()).split("-")
		county=location[1][1:len(location[1])-1]
		province=location[2][1:]

		location_detail= self.convert_unicode("".join(response.xpath(".//div[@class='detail_khungxam']")[1].xpath(".//div")[1].xpath(".//text()").extract()))
		if re.search('Thuoc du an',location_detail):
			location_detail=location_detail[:re.search('Thuoc du an',location_detail).start()]
		if county.split(" ")[1].isdigit()==False:
			county=" ".join(county.split(" ")[1:len(county.split(" "))])
		if province=="Ho Chi Minh":
			province="HCM"

		info_no_1= response.xpath(".//ul[@class='info_no1']/li/span")
		area= self.convert_unicode(info_no_1[1].xpath("./b/text()").extract_first())
		raw_price= self.convert_unicode(info_no_1[0].xpath("./b/text()").extract_first())
		price=raw_price
		if raw_price.split(" ")[0].isdigit():
			base=float(raw_price.split(" ")[0])
			unit=raw_price.split(" ")[1]
			multiply=1
			if unit[0]=="T":
				if unit[1]=='r':
					multiply=1000000
				elif unit[1]=='y':
					multiply=1000000000
			elif unit[0]=='N':
				multiply=1000
			price=str(int(base*multiply))

		yield {
			'post-id': post_id,
			'website': "123nhadata.vn",
			'author': author,
			'post-time': {'date': last_update_time.strftime("%d-%m-%Y"),'weekday': last_update_time.weekday()},
			'title': title,
			'location': {'county': county,'province': province,'location-detail':location_detail},
			'area':area,
			'price':price,
			'transaction-type': transaction_type,
			'house-type': {'general':"",'detailed':house_type},
			'description': description
		}

	def parse(self,response):
		is_last= False
		items=response.xpath(".//div[@class='box_nhadatban ']")
		global cur_page_index
		if response.url.split("/")[len(response.url.split("/"))-1].isdigit() == False:
			global last_post_time
			cur_page_index=1
			with open('last_post_id.json','r+') as f:
				data=json.load(f)

				last_post_time=''
				if "123nhadat" in data:
					last_post_time=datetime.datetime.strptime(data["123nhadat"],"%d-%m-%Y %H:%M")
				data["123nhadat"]=(datetime.datetime.now()-datetime.timedelta(minutes=15)).strftime("%d-%m-%Y %H:%M")
			os.remove('last_post_id.json')
			with open('last_post_id.json','w') as f:
				json.dump(data,f,indent = 4)
		for item in items:
			post_id=self.convert_unicode(item.xpath("./div/div/span/text()").extract_first().split(' ')[1])
			post_time_text=self.convert_unicode(item.xpath("./div/div/div/ul/li/span/span/text()").extract_first())
			post_time=self.convert_time(post_time_text,item)
			if post_time<=last_post_time:
				is_last=True
				break
			item_url=self.convert_unicode(item.xpath("./div/h4/a/@href").extract_first())
			yield scrapy.Request(item_url,callback=self.parse_item)



		is_last_page=False
		paging=response.xpath(".//ul[contains(@class,'pagging')]/li/a/text()").extract()
		if paging[len(paging)-1]!='Sau':
			is_last_page=True
		if is_last == False and is_last_page== False:
			
			cur_page_index+=1
			yield scrapy.Request("http://123nhadat.vn/raovat-c2/nha-dat-cho-thue-tai-tp-hcm-3/" + str(cur_page_index)+"/-1/0/0", callback= self.parse)
		

	def __repr__(self):
		"""only print out attr1 after exiting the Pipeline"""
		return repr({})