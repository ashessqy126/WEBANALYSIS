#encoding=utf-8
import scrapy
from scrapy.http import Request
import re
from scrapy.utils.url import urljoin_rfc
import hashlib
import os
class srcSpider(scrapy.Spider):
	name = "srcspider"
	MAXBYTES = 70000
	def __init__ (self,website,domain):
		self.start_urls=[]
		self.start_urls.append(website)
		self.host = website.lstrip("http://")
		self.host = self.host.rstrip("/")
		self.domain = domain
	def ishtml(self,response):
		headurl = response.body[:20]
		pattern = re.compile("<!DOCTYPE html",re.I)
		match = pattern.search(response.body)
		#是html
		if match:
			return 0
		#不是html
		else:
			return 1
	def ishtmlurl(self,url):
		seg = url.split("/")
		#是html
		if seg[-1]=='':
			return 0
		else:
			index = seg[-1].find(".")
			index1 = seg[-1].find(".html")
			#不是html
			if index>=0 and index1==-1:
				return 1
			#是html
			else:
				return 0
	def parse(self,response):
		print 'parsing',response.url
		result = self.ishtml(response)
		if result==0:
			src_sels = response.xpath("//@src").extract()
			for src_sel in src_sels:
				itemsrc = urljoin_rfc(response.url,src_sel)
				yield Request(itemsrc,headers={'Host':'caffe.berkeleyvision.org','User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"},callback=self.download)
			href_sels = response.xpath("//a/@href").extract()
			for href_sel in href_sels:
				pattern = re.compile(self.domain)
				match = pattern.search(response.url)
				result1 = self.ishtmlurl(href_sel)
				if match and result1==0:
					yield Request(urljoin_rfc(response.url,href_sel),headers={'Host':self.host,'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"},callback=self.parse)
	def download(self,response):
		if len(response.body)>self.MAXBYTES:
			print 'download',response.url
			m = hashlib.md5()
			m.update(self.start_urls[0])
			newdir = 'sources/' + m.hexdigest()
			if not os.path.isdir(newdir):
				os.mkdir(newdir)
			filename = os.path.join(newdir,response.url.split("/")[-1])
			f = open(filename,"wb+")
			f.write(response.body)
			f.close()
	