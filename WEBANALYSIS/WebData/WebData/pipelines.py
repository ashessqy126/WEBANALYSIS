# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi
import MySQLdb.cursors
import logging
class WebdataPipeline(object):
	def __init__(self):
		self.dbpool = adbapi.ConnectionPool('MySQLdb', db='webdata',
                user='root', passwd='13398303582song', cursorclass=MySQLdb.cursors.DictCursor,
                charset='utf8', use_unicode=True)
	def open_spider(self,spider):
		self.website = spider.start_urls[0]
		#if spider.name == 'codespider':
			#query = self.dbpool.runInteraction(self._conditional_clearmatch)
			#query.addErrback(self.handle_error)
	def process_item(self, item, spider):
        # run db query in thread pool 
		if spider.name=='linkspider':
			query = self.dbpool.runInteraction(self._conditional_insertlink,item)
			query.addErrback(self.handle_error)
		elif spider.name=='codespider':
			query = self.dbpool.runInteraction(self._conditional_insertmatch,item)
			query.addErrback(self.handle_error)
		return item
	def _conditional_insertlink(self, tx, item):
		# create record if doesn't exist.
        # all this block run on it's own thread
		query = "select * from links where link=%s and website=%s;"
		tx.execute(query,(item['link'],self.website))
		result = tx.fetchone()
		if result:
			print "Item already stored in db: %s" % item
		else:
			tx.execute("insert into links (link, website) values (%s, %s) ON DUPLICATE KEY UPDATE count=count+1;",(item['link'],self.website))
          	print "Item stored in db: %s" % item
	def handle_error(self, e):
		print e
	def _conditional_insertmatch(self,tx,item):
		query = "insert into matchresult(code,degree,website) values(%s, %s, %s) ON DUPLICATE KEY UPDATE count=count+1;"
		tx.execute(query,(item['code'],item['degree'],self.website))
		print "match result has been stored..."
	def _conditional_clearmatch(self,tx):
		query = 'delete from matchresult where website=%s'
		tx.execute(query,self.website)
		print "matchresult stored start..."