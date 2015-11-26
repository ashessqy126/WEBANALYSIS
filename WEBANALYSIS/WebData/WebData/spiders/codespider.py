#encoding=utf-8
import scrapy
from scrapy.http import Request
import re
from scrapy.utils.url import urljoin_rfc
import MySQLdb
from WebData.items import MatchItem
class codeSpider(scrapy.Spider):
	name = "codespider"
	allowed_domains=["berkeleyvision.org"]
	MAXBYTES = 70000
	def __init__(self,website,domain):
		self.start_urls=[]
		self.allowed_domains = []
		self.start_urls.append(website)
		self.host = website.lstrip("http://")
		self.host = self.host.rstrip("/")
		self.allowed_domains.append(domain)
		con = MySQLdb.connect('localhost','root','13398303582song','webdata')
		cur = con.cursor(cursorclass=MySQLdb.cursors.DictCursor)
		cur.execute("select * from codes")
		self.htmlfeatures=cur.fetchall()
		cur.execute("select * from codes where flag='css'")
		self.cssfeatures=cur.fetchall()
		cur.execute("select * from codes where flag='js'")
		self.jsfeatures=cur.fetchall()
		con.close()
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
		item = MatchItem()
		result = self.ishtml(response)
		if result==0:
			if self.htmlfeatures:
				for htmlfeature in self.htmlfeatures:
					pattern = re.compile(htmlfeature['code'])
					match = pattern.search(response.body)
					if match:
						item['code']=match.group()
						item['degree']=htmlfeature['degree']
						yield item
				#递归爬取网页
				links = response.xpath("//a/@href").extract()
				scripts = response.xpath("//script/@src").extract()
				csses = response.xpath("//link/@href").extract()
				for script in scripts:
					yield Request(urljoin_rfc(response.url,script),headers={'Host':self.host,'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"},callback=self.scriptparse)
				for css in csses:
					yield Request(urljoin_rfc(response.url,css),headers={'Host':self.host,'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"},callback=self.cssparse)
				for link in links:
					result1 = self.ishtmlurl(link)
					if result1 == 0:
						yield Request(urljoin_rfc(response.url,link),headers={'Host':self.host,'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36"},callback=self.parse)
	def scriptparse(self,response):
		item = MatchItem()
		if self.jsfeatures:
			for scriptfeature in self.jsfeatures:
				pattern = re.compile(scriptfeature['code'])
				match = pattern.search(response.body)
				if match:
					item['code']=match.group()
					item['degree']=scriptfeature['degree']
					yield item
	def cssparse(self,response):
		item = MatchItem()
		if self.cssfeatures:
			for cssfeature in self.cssfeatures:
				pattern = re.compile(cssfeature['code'])
				match = pattern.search(response.body)
				if match:
					item['code']=match.group()
					item['degree']=cssfeature['degree']
					yield item