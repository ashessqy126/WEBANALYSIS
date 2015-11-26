#encoding=utf-8
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from multiprocessing import Process, Queue  
import threading
import time
def startprocess(queue):
	runner = CrawlerRunner(get_project_settings())
	dfs = set()
	
	l = runner.crawl('linkspider', website='http://caffe.berkeleyvision.org/', domain='berkeleyvision.org').addCallback(test,queue)
			#回调函数中参数1表示linkspider
	dfs.add(l)
	
	s = runner.crawl('srcspider', website='http://caffe.berkeleyvision.org/', domain='berkeleyvision.org').addCallback(test,queue)#回调函数中参数2表示srcspider
	dfs.add(s)
	c = runner.crawl('codespider', website='http://caffe.berkeleyvision.org/', domain='berkeleyvision.org').addCallback(test,queue)#回调函数中参数3表示codespider
	dfs.add(c)
	defer.DeferredList(dfs).addBoth(lambda _: reactor.stop())
			# the script will block here until all crawling jobs are finished
	reactor.run()
class listenTread(threading.Thread):
	def __init__(self,queue):
		self.queue = queue
		threading.Thread.__init__(self)
		self.flag = 0
	def run(self):
		try:
			while (self.flag != 3):
				a=self.queue.get()
				if a!=0:
					self.flag = self.flag + a
					print '*********************************************************************************************'
		except Exception,e:
			print e
def test(content,queue):
	queue.put(1)
if __name__ == '__main__':  
	q = Queue()  
	p = Process(target=startprocess, args=(q,))
	p.start()
	listener = listenTread(q)
	listener.start()
	while(1):
		time.sleep(1)
		print "haha"
		print listener.flag
