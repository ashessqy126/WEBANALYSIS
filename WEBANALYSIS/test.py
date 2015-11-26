runner = CrawlerRunner(get_project_settings())
dfs = set()
l = runner.crawl('linkspider', website=self.website, domain=self.domain).addCallback(self.setflag,1).addErrback(self.erro,-1)
			#回调函数中参数1表示linkspider
dfs.add(l)
s = runner.crawl('srcspider', website=self.website, domain=self.domain).addCallback(self.setflag,1).addErrback(self.erro,-1)#回调函数中参数2表示srcspider
dfs.add(s)
c = runner.crawl('codespider', website=self.website, domain=self.domain).addCallback(self.setflag,1).addErrback(self.erro,-1)#回调函数中参数3表示codespider
dfs.add(c)
defer.DeferredList(dfs).addBoth(lambda _: reactor.stop())
			# the script will block here until all crawling jobs are finished
reactor.run()