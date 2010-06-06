from Queue import Queue
import Pyro

class DispatcherQueue(object):
	def __init__(self):
		self.workqueue = Queue()
		self.resultqueue = Queue()
	def putWork(self, item):
		self.workqueue.put(item)
	def getWork(self, timeout=5):
		return self.workqueue.get(block=True, timeout=timeout)
	def putResult(self, item):
		self.resultqueue.put(item)
	def getResult(self, timeout=5):
		return self.resultqueue.get(block=True, timeout=timeout)
	def workQueueSize(self):
		return self.workqueue.qsize()
	def resultQueueSize(self):
		return self.resultqueue.qsize()
		
######## main program

ns=Pyro.naming.locateNS()
daemon=Pyro.core.Daemon()
dispatcher=DispatcherQueue()
uri=daemon.register(dispatcher)
ns.remove("example.distributed.dispatcher")
ns.register("example.distributed.dispatcher", uri)
print "Dispatcher is ready."
daemon.requestLoop()
