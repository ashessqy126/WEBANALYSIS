from webcrawl import *
import time
flag = 0
webc = webcrawl('http://caffe.berkeleyvision.org/','berkeleyvision.org')
webc.run()
flag = webc.flag
print flag
time.sleep(120)
flag = webc.flag
if flag!=0:
	print "************************************************"
time.sleep(180)
flag = webc.flag
if flag!=0:
	print "*************************************************"
time.sleep(480)
flag = webc.flag
if flag!=0:
	print "*************************************************"