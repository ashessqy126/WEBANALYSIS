#encoding=utf-8
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import threading
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
import threading
import random
from checkurl import searchlink
from WebModuel.models import *
import hashlib
import os
import pyclamav
from multiprocessing import Process, Queue  
import psutil
import datetime
from django.shortcuts import render

def setflag(content,queue):
	queue.put(1)
def err(content,queue):
	queue.put(-1)
def webcrawl(queue,webs,dom):
	website = ''
	domain = ''
	try:
		runner = CrawlerRunner(get_project_settings())
		dfs = set()
		l = runner.crawl('linkspider', website=webs, domain=dom).addCallback(setflag, queue).addErrback(err, queue)
			#回调函数中参数1表示linkspider
		dfs.add(l)
		s = runner.crawl('srcspider',  website=webs, domain=dom).addCallback(setflag, queue).addErrback(err, queue)#回调函数中参数2表示srcspider
		dfs.add(s)
		c = runner.crawl('codespider', website=webs, domain=dom).addCallback(setflag, queue).addErrback(err, queue)#回调函数中参数3表示codespider
		dfs.add(c)
		defer.DeferredList(dfs).addBoth(lambda _: reactor.stop())
			# the script will block here until all crawling jobs are finished
		reactor.run()
	except Exception,e:
		print e
class crawllistenThreading(threading.Thread):
	def __init__(self, queue):
		threading.Thread.__init__(self)
		self.queue = queue
		self.flag = 0
	def getflag(self):
		return self.flag
	def run(self):
		try:
			self.flag = 1
			while (self.flag != 4 and self.flag != -1):
				status = self.queue.get()
				if status != -1:
					self.flag = self.flag + status
				else:
					self.flag = -1
		except Exception,e:
			print e

class scanvirusThreading(threading.Thread):
	def __init__(self,website):
		self.rootdir = 'sources'
		self.result = []
		self.allcount = 0
		self.count = 0
		self.dangercount = 0
		threading.Thread.__init__(self)
		m = hashlib.md5()
		m.update(website)
		self.userdir = os.path.join(self.rootdir, m.hexdigest())
	def getret(self):
		return self.result
	def getallcount(self):
		return self.allcount
	def getcount(self):
		return self.count
	def getdangercount(self):
		return self.dangercount
	def run(self):
		try:
			for parent,dirnames,filenames in os.walk(self.userdir):
				self.allcount = len(filenames)
				for filename in filenames:       #输出文件信息
					ret = []
					tmp = {}
					print "scan file:" + os.path.join(parent,filename) 
					ret = pyclamav.scanfile(os.path.join(parent,filename))
					if ret[0]!=0:
						tmp['file'] = os.path.join(parent,filename)
						tmp['virusinfo'] = ret[1:]
						self.result.append(tmp)
						self.dangercount = self.dangercount + 1
					self.count = self.count + 1
		except Exception,e:
			print e

class checkurlThreading(threading.Thread):
	def __init__(self,website):
		threading.Thread.__init__(self)
		self.website = website
		self.count = 0
		self.dangercount = 0
		self.allcount = 0
		self.result = []
		self.link = ''
	def getcount(self):
		return self.count
	def getdangercount(self):
		return self.dangercount
	def getallcount(self):
		return self.allcount
	def getresult(self):
		return self.result
	def getlink(self):
		return self.link
	def run(self):
		try:
			urlists = Links.objects.filter(website = self.website)
			self.allcount = urlists.count()
			for urlist in urlists:
				print "check:"+urlist.link
				flag = searchlink(urlist.link)
				self.link = urlist.link
				if flag == 1:
					tmp = {}
					tmp['degree'] = 'phinish website'
					tmp['degreenum'] = 1
					tmp['url'] = urlist.link
					self.dangercount = self.dangercount + 1
					self.result.append(tmp)
					print "phinish website:"+urlist.link
				elif flag == 2:
					tmp = {}
					tmp['degree'] = 'danger website'
					tmp['degreenum'] = 2
					tmp['url'] = urlist.link
					self.dangercount = self.dangercount + 1
					self.result.append(tmp)
					print "danger website:" + urlist.link
				self.count = self.count + 1
		except Exception,e:
			self.result = None
			print e

webcrawlpool = {}
scanlinkpool = {}
scansrcpool = {}
removepool ={}
def index(request):
	return render(request,'index.html')
def startscan(request):
	responsedata={}
	website = request.GET.get("website")
	domain = request.GET.get("domain")
	if website and domain:
		#抓取池里面没有监听线程，或者抓取工作已经完成
		if not webcrawlpool.get(request.session.get('id')) or (webcrawlpool.get(request.session.get('id')) and request.session.get("completed") == True):
			if webcrawlpool.get(request.session.get('id')):
				webcrawlpool.get(request.session.get('id')+'pro').terminate()
				webcrawlpool.get(request.session.get('id')+'pro').join()
			id = str(random.random()*1000)
			request.session['id'] = id
			request.session['completed'] = False
			log = request.META['REMOTE_ADDR']
			time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			log = log + ':' + website+'---'+time+'\n'
			f = open('log/CrawlWeb_Log','ab+')
			f.write(log)
			f.close()
			webcrawlpool[request.session.get('id')+'queue'] = Queue()
			webcrawlpool[request.session.get('id')] = crawllistenThreading(webcrawlpool.get(request.session.get('id')+'queue'))
			webcrawlpool[request.session.get('id')+'pro'] = Process(target=webcrawl, args=(webcrawlpool.get(request.session.get('id')+'queue'),website,domain))
			webcrawlpool.get(request.session.get('id')+'pro').start()
			webcrawlpool.get(request.session.get('id')).start()
			responsedata['status'] = 0
		else:
			responsedata['status'] = -2
			responsedata['error'] = 'please wait..'
	else:
		responsedata['status']=-1
		responsedata['error']='you should input the website and domain'
	return HttpResponse(json.dumps(responsedata),content_type="application/json")

def checkflag(request):
	responsedata = {}
	if request.session.get('completed') == False:
		try:
			flag = webcrawlpool.get(request.session.get('id')).getflag()
			if flag==0:
				#初始化
				request.session['completed'] = False
				responsedata['status']=0
			elif flag == 1:
				#开始抓取
				request.session['completed'] = False
				responsedata['status']=1
			elif flag==2:
				#第一工作已经完成，第二工作开始
				request.session['completed'] = False
				responsedata['status']=2
			elif flag==3:
				#第二工作已经完成，第三工作开始
				request.session['completed'] = False
				responsedata['status']=3
			elif flag == 4:
				#所有工作已经完成
				responsedata['status'] = 4
				responsedata['completed']='just finished'
				request.session['completed'] = True
			else:
				#错误
				responsedata['status'] = flag
				responsedata['error']='crawl error'
		except Exception,e:
			responsedata['status'] = -2
			responsedata['error'] = "threading just start..."
	else:
		responsedata['status'] = 4
		responsedata['completed']='finished'
	return HttpResponse(json.dumps(responsedata),content_type="application/json")

def start_analysis_link(request):
	responsedata={}
	website = request.GET.get("website")
	if request.session.get("completed") == False:
		responsedata['status'] = -1
		responsedata['error'] = 'not finished'
	else:
		try:
			log = request.META['REMOTE_ADDR']
			time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			log = log + ':' + website+'---'+time+'\n'
			f = open('log/LinkAna_Log','ab+')
			f.write(log)
			f.close()
			scanlinkpool[request.session.get('id')] = checkurlThreading(website)
			scanlinkpool[request.session.get('id')].start()
			responsedata['status'] = 0
		except:
			responsedata['status'] = -2
			responsedata['error'] = 'interupt'
	return HttpResponse(json.dumps(responsedata),content_type="application/json")

def get_analysis_link(request):
	responsedata = {}
	if request.session.get("completed") == False: #and webcrawlpool.get(request.session.get('id')):
		responsedata['status'] = -1
		responsedata['error'] = 'not finished'
	else:
		checkurl = scanlinkpool.get(request.session.get('id'))
		if checkurl:
			count = checkurl.getcount()
			dangercount = checkurl.getdangercount()
			allcount = checkurl.getallcount()
			link = checkurl.getlink()
			if count == allcount:
				responsedata['status'] = 1
				responsedata['results'] = checkurl.getresult()
			else:
				responsedata['status'] = 0
				responsedata['results'] = checkurl.getresult()
			responsedata['allcount'] = allcount
			responsedata['count'] = count
			responsedata['dangercount'] = dangercount
			responsedata['link'] = link
		else:
			#线程已结束
			responsedata['status'] = -2
			responsedata['error'] = 'threading exits'
	return HttpResponse(json.dumps(responsedata),content_type="application/json")

def start_scansrc(request):
	rootdir = '../sources'
	responsedata={}
	website = request.GET.get("website")
	if not website:
		responsedata['status'] = -3
		responsedata['error'] = 'you should input the website'
	else:
		if request.session.get("completed") == False:
			responsedata['status'] = -1
			responsedata['error'] = 'not finished'
		else:
			try:
				log = request.META['REMOTE_ADDR']
				time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
				log = log + ':' + website+'---'+time+'\n'
				f = open('log/ScanSrc_Log','ab+')
				f.write(log)
				f.close()
				scansrcpool[request.session.get('id')] = scanvirusThreading(website)
				scansrcpool.get(request.session.get('id')).start()
				responsedata['status'] = 0
			except Exception,e:
				responsedata['status'] = -2
				responsedata['error'] = 'interupt'
				print e
	return HttpResponse(json.dumps(responsedata),content_type="application/json")

def get_scansrc_status(request):
	responsedata = {}
	if request.session.get("completed") == False:
		responsedata['status'] = -1
		responsedata['error'] = 'not finished'
	else:
		scanfiles = scansrcpool.get(request.session.get('id'))
		if scanfiles:
			count = scanfiles.getcount()
			allcount = scanfiles.getallcount()
			ret = scanfiles.getret()
			dangercount = scanfiles.getdangercount()
			if count == allcount:
				responsedata['status'] = 1
			else:
				responsedata['status'] = 0
			responsedata['allcount'] = allcount
			responsedata['count'] = count
			responsedata['result'] = ret
			responsedata['dangercount'] = dangercount
		else:
			responsedata['status'] = -2
			responsedata['error'] = 'threading exits'
	return HttpResponse(json.dumps(responsedata),content_type="application/json")

def badcode(request):
	responsedata={}
	result = []
	website = request.GET.get("website")
	if request.session.get("completed") == False:
		responsedata['status'] = -1
		responsedata['error'] = 'not finished'
	else:
		if website:
			log = request.META['REMOTE_ADDR']
			time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			log = log + ':' + website+'---'+time+'\n'
			f = open('log/BadCode_Log','ab+')
			f.write(log)
			f.close()
			mresults = Matchresult.objects.filter(website=website)
			for mresult in mresults:
				tmp = {}
				tmp['warningcode'] = mresult.code
				tmp['degree'] = mresult.degree
				tmp['count'] = mresult.count
				result.append(tmp)
			responsedata['status']=0
			responsedata['result']=result
		else:
			responsedata['status'] = -2
			responsedata['error'] = 'you should must input website'
	return HttpResponse(json.dumps(responsedata),content_type="application/json")

def removeCaches(request):
	responsedata = {}
	flag = 0
	website = request.GET.get("website")
	caches = Links.objects.filter(website = website)
	m = hashlib.md5()
	m.update(website)
	targetdir = os.path.join('sources', m.hexdigest())
	if os.path.isdir(targetdir):
		for file in os.listdir(targetdir):
			targetfile = os.path.join(targetdir, file)
			if os.path.isfile(targetfile):
				os.remove(targetfile)
				flag = 1
	if caches:
		responsedata['status'] = 0
		caches.delete()
	elif flag == 0:
		responsedata['status'] = -1
		responsedata['error'] = "don't exits this cache"
	else:
		responsedata['status'] = 0
	return HttpResponse(json.dumps(responsedata),content_type="application/json")
def watchsys(request):
	responsedata = {}
	try:
		cpu_percent = psutil.cpu_percent()
		responsedata['cpu_percent'] = cpu_percent
		mem_percent = psutil.virtual_memory().percent
		responsedata['mem_percent'] = mem_percent
		swap_percent = psutil.swap_memory().percent
		responsedata['swap_percent'] = swap_percent
		disk_usage = psutil.disk_usage("/").percent
		responsedata['disk_usage'] = disk_usage
		if cpu_percent > 90:
			responsedata['status'] = 4
			responsedata['info'] = 'very danger'
		elif mem_percent >80:
			responsedata['status'] = 3
			responsedata['info'] = 'danger'
		elif disk_usage > 80:
			responsedata['status'] = 2
			responsedata['info'] = 'warning'
 		elif swap_percent > 50:
 			responsedata['status'] = 1
 			responsedata['info'] = 'little warning'
 		else:
 			responsedata['status'] = 0
 			responsedata['info'] = 'normal'
 		responsedata['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	except Exception, e:
		responsedata['status'] = -1
		responsedata['error'] = 'watch error'
	return HttpResponse(json.dumps(responsedata),content_type="application/json")