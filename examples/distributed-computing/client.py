#!/usr/bin/env python
import Pyro.core
import Queue
import random
from workitem import Workitem

NUMBER_OF_ITEMS = 40


def main():	
	print "\nThis program will calculate Prime Factorials of a bunch of random numbers."
	print "The more workers you will start (on different cpus/cores/machines),"
	print "the faster you will get the complete list of results!\n"
	with Pyro.core.Proxy("PYRONAME:example.distributed.dispatcher") as dispatcher:
		placework(dispatcher)
		numbers=collectresults(dispatcher)
	printresults(numbers)
		
def placework(dispatcher):
	print "placing work items into dispatcher queue."
	for i in range(NUMBER_OF_ITEMS):
		number=random.randint(3211, 5000)*random.randint(177,3000)*37
		item = Workitem(i+1, number)
		dispatcher.putWork(item)

def collectresults(dispatcher):
	print "getting results from dispatcher queue."
	numbers={}
	while len(numbers)<NUMBER_OF_ITEMS:
		try:
			item = dispatcher.getResult()
			print "Got result: %s (from %s)" % (item, item.processedBy)
			numbers[item.data] = item.result
		except Queue.Empty:
			print "Not all results available yet (got %d out of %d). Work queue size: %d" %  \
					(len(numbers),NUMBER_OF_ITEMS,dispatcher.workQueueSize())
	
	if dispatcher.resultQueueSize()>0:
		print "there's still stuff in the dispatcher result queue, that is odd..."
	return numbers

def printresults(numbers):
	print "\nComputed Prime Factorials follow:"
	for (number, factorials) in numbers.items():
		print number,"-->",factorials

if __name__=="__main__":
	main()
