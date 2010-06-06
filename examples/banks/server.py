#
#	The banks server
#

import sys
import Pyro
import banks

ns=Pyro.naming.locateNS()
daemon=Pyro.core.Daemon()
ns.remove("example.banks.rabobank")
ns.remove("example.banks.abn")

uri=daemon.register(banks.Rabobank())
ns.register("example.banks.rabobank",uri)
uri=daemon.register(banks.ABN())
ns.register("example.banks.abn",uri)

print "available banks:"
print ns.list(prefix="example.banks.").keys()

# enter the service loop.
print 'Banks are ready for customers.'
daemon.requestLoop()
