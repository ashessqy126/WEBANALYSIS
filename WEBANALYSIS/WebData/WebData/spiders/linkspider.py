#encoding=utf-8
import scrapy
from scrapy.http import Request
import re
from scrapy.utils.url import urljoin_rfc
from WebData.items import LinkItem
import time
import hashlib
import os
class linkSpider(scrapy.Spider):
	name = "linkspider"
	allowed_domains=["berkeleyvision.org"]
	MAXBYTES = 70000
	def __init__ (self,website,domain):
		self.start_urls = []
		self.allowed_domains = []
		self.start_urls.append(website)
		self.host = website.lstrip("http://")
		self.host = self.host.rstrip("/")
		self.allowed_domains.append(domain)
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
	def parse(self,response):
		print 'parsing',response.url
		q = self.ishtml(response)
		if q == 1:
			if len(response.body)>=self.MAXBYTES:
				m = hashlib.md5()
				m.update(self.start_urls[0])
				newdir = 'sources/' + m.hexdigest()
				if not os.path.isdir(newdir):
					os.mkdir(newdir)
				seg = response.url.split("/")
				if seg[-1]=='':
					filename = os.path.join(newdir, seg[-2])
				else:
					filename = os.path.join(newdir, seg[-1])
				f = open(filename,"wb+")
				f.write(response.body)
				f.close()
		elif q == 0:
			item = LinkItem()
			href_sels = response.xpath("//a/@href").extract();
			for href_sel in href_sels:
				link = ""
				if href_sel.find("http://")==-1 and href_sel.find("https://")==-1:
					link = urljoin_rfc(response.url,href_sel)
					item['link'] = link
				else:
					link = href_sel
					item['link'] = link;
				yield Request(link, headers={'Host':self.host,'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"},callback=self.parse)
				time.sleep(0.008)
				yield item;

	