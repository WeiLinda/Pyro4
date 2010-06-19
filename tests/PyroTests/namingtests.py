"""
Tests for the name server (online/running).

Pyro - Python Remote Objects.  Copyright by Irmen de Jong.
irmen@razorvine.net - http://www.razorvine.net/python/Pyro
"""

from __future__ import with_statement
import unittest
import time, socket
import Pyro.config
import Pyro.core
import Pyro.naming
import Pyro.socketutil
from Pyro.errors import NamingError
from Pyro import threadutil

class NSLoopThread(threadutil.Thread):
    def __init__(self, nameserver):
        super(NSLoopThread,self).__init__()
        self.setDaemon(True)
        self.nameserver=nameserver
        self.running=threadutil.Event()
        self.running.clear()
    def run(self):
        self.running.set()
        self.nameserver.requestLoop()

class BCSetupTests(unittest.TestCase):
    def testBCstart(self):
        myIpAddress=Pyro.socketutil.getMyIpAddress(workaround127=True)
        nsUri, nameserver, bcserver = Pyro.naming.startNS(host=myIpAddress, port=0, bcport=0, enableBroadcast=False)
        self.assertTrue(bcserver is None)
        nameserver.close()
        nsUri, nameserver, bcserver = Pyro.naming.startNS(host=myIpAddress, port=0, bcport=0, enableBroadcast=True)
        self.assertTrue(bcserver is not None, "expected a BC server to be running. Check DNS setup (hostname must not resolve to loopback address")
        self.assertTrue(bcserver.fileno() > 1)
        self.assertTrue(bcserver.sock is not None)
        nameserver.close()
        bcserver.close()

class NameServerTests(unittest.TestCase):
    def setUp(self):
        Pyro.config.POLLTIMEOUT=0.1
        myIpAddress=Pyro.socketutil.getMyIpAddress(workaround127=True)
        self.nsUri, self.nameserver, self.bcserver = Pyro.naming.startNS(host=myIpAddress, port=0, bcport=0)
        self.assertTrue(self.bcserver is not None,"expected a BC server to be running")
        self.bcserver.runInThread()
        self.daemonthread=NSLoopThread(self.nameserver)
        self.daemonthread.start()
        self.daemonthread.running.wait()
        self.old_bcPort=Pyro.config.NS_BCPORT
        self.old_nsPort=Pyro.config.NS_PORT
        Pyro.config.NS_PORT=self.nsUri.port
        Pyro.config.NS_BCPORT=self.bcserver.getPort()
    def tearDown(self):
        time.sleep(0.1)
        self.nameserver.shutdown()
        self.bcserver.close()
        self.daemonthread.join()
        Pyro.config.NS_PORT=self.old_nsPort
        Pyro.config.NS_BCPORT=self.old_bcPort
   
    def testLookupAndRegister(self):
        original_nshost=Pyro.config.NS_HOST
        try:
            Pyro.config.NS_HOST=socket.gethostname()
            ns=Pyro.naming.locateNS() # broadcast lookup
            self.assertTrue(isinstance(ns, Pyro.core.Proxy))
            ns._pyroRelease()
            ns=Pyro.naming.locateNS(self.nsUri.host) # normal lookup
            self.assertTrue(isinstance(ns, Pyro.core.Proxy))
            uri=ns._pyroUri
            self.assertEqual("PYRO",uri.protocol)
            self.assertEqual(self.nsUri.host,uri.host)
            self.assertEqual(Pyro.config.NS_PORT,uri.port)
            ns._pyroRelease()
            ns=Pyro.naming.locateNS(self.nsUri.host,Pyro.config.NS_PORT)
            uri=ns._pyroUri
            self.assertEqual("PYRO",uri.protocol)
            self.assertEqual(self.nsUri.host,uri.host)
            self.assertEqual(Pyro.config.NS_PORT,uri.port)
        finally:
            Pyro.config.NS_HOST=original_nshost
        
        # check that we cannot register a stupid type
        self.assertRaises(TypeError, ns.register, "unittest.object1", 5555)
        # we can register str or URI, lookup always returns URI        
        ns.register("unittest.object2", "PYRO:55555@host.com:4444")
        self.assertEquals(Pyro.core.URI("PYRO:55555@host.com:4444"), ns.lookup("unittest.object2"))
        ns.register("unittest.object3", Pyro.core.URI("PYRO:66666@host.com:4444"))
        self.assertEquals(Pyro.core.URI("PYRO:66666@host.com:4444"), ns.lookup("unittest.object3"))
        
        # check that the non-socket locations are not yet supported  
        self.assertRaises(NotImplementedError, Pyro.naming.locateNS, "./p:pipename")
        #ns=Pyro.naming.locateNS("./p:pipename")
        #uri=ns._pyroUri
        #self.assertEqual("PYRO",uri.protocol)
        #self.assertEqual("pipename",uri.pipename)
        ns._pyroRelease()

    def testDaemonPyroObj(self):
        uri=self.nsUri
        uri.object=Pyro.constants.DAEMON_NAME
        with Pyro.core.Proxy(uri) as daemonobj:
            daemonobj.ping()
            daemonobj.registered()
            try:
                daemonobj.shutdown()
                self.fail("should not succeed to call unexposed method on daemon")
            except AttributeError:
                pass
        
    def testMulti(self):
        uristr=str(self.nsUri)
        p=Pyro.core.Proxy(uristr)
        p._pyroBind()
        p._pyroRelease()
        uri=Pyro.naming.resolve(uristr)
        p=Pyro.core.Proxy(uri)
        p._pyroBind()
        p._pyroRelease()
        uri=Pyro.naming.resolve(uristr)
        p=Pyro.core.Proxy(uri)
        p._pyroBind()
        p._pyroRelease()
        uri=Pyro.naming.resolve(uristr)
        p=Pyro.core.Proxy(uri)
        p._pyroBind()
        p._pyroRelease()
        uri=Pyro.naming.resolve(uristr)
        p=Pyro.core.Proxy(uri)
        p._pyroBind()
        p._pyroRelease()
        uri=Pyro.naming.resolve(uristr)
        p=Pyro.core.Proxy(uri)
        p._pyroBind()
        p._pyroRelease()
        daemonUri="PYRO:"+Pyro.constants.DAEMON_NAME+"@"+uri.location
        uri=Pyro.naming.resolve(daemonUri)
        uri=Pyro.naming.resolve(daemonUri)
        uri=Pyro.naming.resolve(daemonUri)
        uri=Pyro.naming.resolve(daemonUri)
        uri=Pyro.naming.resolve(daemonUri)
        uri=Pyro.naming.resolve(daemonUri)
        uri=Pyro.naming.resolve(daemonUri)
        pyronameUri="PYRONAME:"+Pyro.constants.NAMESERVER_NAME+"@"+uri.location
        uri=Pyro.naming.resolve(pyronameUri)
        uri=Pyro.naming.resolve(pyronameUri)
        uri=Pyro.naming.resolve(pyronameUri)
        uri=Pyro.naming.resolve(pyronameUri)
        uri=Pyro.naming.resolve(pyronameUri)
        uri=Pyro.naming.resolve(pyronameUri)
    
    def testResolve(self):
        resolved1=Pyro.naming.resolve(Pyro.core.URI("PYRO:12345@host.com:4444"))
        resolved2=Pyro.naming.resolve("PYRO:12345@host.com:4444")
        self.assertTrue(type(resolved1) is Pyro.core.URI)
        self.assertEqual(resolved1, resolved2)
        self.assertEqual("PYRO:12345@host.com:4444", str(resolved1))
        
        ns=Pyro.naming.locateNS(self.nsUri.host, self.nsUri.port)
        uri=Pyro.naming.resolve("PYRONAME:"+Pyro.constants.NAMESERVER_NAME+"@"+self.nsUri.host+":"+str(self.nsUri.port))
        self.assertEqual("PYRO",uri.protocol)
        self.assertEqual(self.nsUri.host,uri.host)
        self.assertEqual(Pyro.constants.NAMESERVER_NAME,uri.object)
        self.assertEqual(uri, ns._pyroUri)
        ns._pyroRelease()

        # broadcast lookup
        self.assertRaises(NamingError, Pyro.naming.resolve, "PYRONAME:unknown_object")
        uri=Pyro.naming.resolve("PYRONAME:"+Pyro.constants.NAMESERVER_NAME)
        self.assertEquals(Pyro.core.URI,type(uri))
        self.assertEquals("PYRO",uri.protocol)

        # test some errors
        self.assertRaises(NamingError, Pyro.naming.resolve, "PYRONAME:unknown_object@"+self.nsUri.host)
        self.assertRaises(TypeError, Pyro.naming.resolve, 999)  #wrong arg type


    def testRefuseDottedNames(self):
        with Pyro.naming.locateNS(self.nsUri.host, self.nsUri.port) as ns:
            # the name server should never have dotted names enabled
            self.assertRaises(AttributeError, ns.namespace.keys)
            self.assertTrue(ns._pyroConnection is not None)
        self.assertTrue(ns._pyroConnection is None)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
