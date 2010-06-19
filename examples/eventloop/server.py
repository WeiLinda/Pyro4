import socket
import time
import select
import sys
import Pyro.core
import Pyro.naming

if sys.version_info<(3,0):
    input=raw_input

servertype=input("Servertype thread/select (t/s)?")
if servertype=='t':
    Pyro.config.SERVERTYPE="thread"
else:
    Pyro.config.SERVERTYPE="select"

hostname=socket.gethostname()

class EmbeddedServer(object):
    def multiply(self, x, y):
        return x*y


print("initializing services... servertype=%s" % Pyro.config.SERVERTYPE)
# start a name server with broadcast server as well
nameserverUri, nameserverDaemon, broadcastServer = Pyro.naming.startNS(host=hostname)
assert broadcastServer is not None, "expect a broadcast server to be created"

print("got a Nameserver, uri=%s" % nameserverUri)
print("ns daemon location string=%s" % nameserverDaemon.locationStr)
print("ns daemon sockets=%s" % nameserverDaemon.sockets())
print("bc server socket=%s (fileno %d)" % (broadcastServer.sock, broadcastServer.fileno()))

# create a Pyro daemon
pyrodaemon=Pyro.core.Daemon(host=hostname)
print("daemon location string=%s" % pyrodaemon.locationStr)
print("daemon sockets=%s" % pyrodaemon.sockets())

# register a server object with the daemon
serveruri=pyrodaemon.register(EmbeddedServer())
print("server uri=%s" % serveruri)

# register it with the embedded nameserver directly
nameserverDaemon.nameserver.register("example.embedded.server",serveruri)

print("")

# below is our custom event loop.
while True:
    print("Waiting for events...")
    # create sets of the socket objects we will be waiting on
    # (a set provides fast lookup compared to a list)
    nameserverSockets = set(nameserverDaemon.sockets())
    pyroSockets = set(pyrodaemon.sockets())
    rs=[broadcastServer]  # only the broadcast server is directly usable as a select() object
    rs.extend(nameserverSockets)
    rs.extend(pyroSockets)
    rs,_,_ = select.select(rs,[],[],3)
    eventsForNameserver=[]
    eventsForDaemon=[]
    for s in rs:
        if s is broadcastServer:
            print("Broadcast server received a request")
            broadcastServer.processRequest()
        elif s in nameserverSockets:
            eventsForNameserver.append(s)
        elif s in pyroSockets:
            eventsForDaemon.append(s)
    if eventsForNameserver:
        print("Nameserver received a request")
        nameserverDaemon.handleRequests(eventsForNameserver)
    if eventsForDaemon:
        print("Daemon received a request")
        pyrodaemon.handleRequests(eventsForDaemon)
        

nameserverDaemon.close()
broadcastServer.close()
pyrodaemon.close()
print("done")
