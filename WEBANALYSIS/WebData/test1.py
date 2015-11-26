from multiprocessing import Queue 

q = Queue()
q.put(1)

p = Queue()
p.put(2)
print p.get()
print q.get()