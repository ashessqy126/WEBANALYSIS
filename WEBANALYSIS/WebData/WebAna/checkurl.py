#encoding=utf-8
import time
import hashlib
import base64
import urllib2
import json
def searchlink(url):
	appkey = 'k-33356'
	secret = 'a176201e188a0969cd7b7fa2ef3c8d14'
	urlbase = base64.b64encode(url)
	signature_base_string = '/phish/?appkey=%s&q=%s&timestamp=%s'%(appkey,urlbase,time.time())
	m1= hashlib.md5()
	m1.update(signature_base_string+secret)
	sign = m1.hexdigest()
	searchurl = "http://open.pc120.com%s&sign=%s"%(signature_base_string,sign)
	data = urllib2.urlopen(searchurl)
	try:
		result = json.loads(data.read())
	except Exception,e:
	#网络错误
		return -3
	#查询错误
	if result['success']==0:
		return -2;
	#查询成功
	else:
		#未知网站
		if result['phish']==-1:
			return -1
		#安全网站
		elif result['phish']==0:
			return 0
		#钓鱼网站
		elif result['phish']==1:
			return 1
		#高风险网站
		elif result['phish']==2:
			return 2
