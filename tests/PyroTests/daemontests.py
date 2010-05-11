from __future__ import with_statement

import unittest
import Pyro.core
import Pyro.constants
import Pyro.config
import Pyro.socketutil
from Pyro.errors import DaemonError,PyroError

class MyObj(object):
    def __init__(self, arg):
        self.arg=arg
    def __eq__(self,other):
        return self.arg==other.arg
    __hash__=object.__hash__

class DaemonTests(unittest.TestCase):
    # We create a daemon, but notice that we are not actually running the requestloop.
    # 'on-line' tests are all taking place in another test, to keep this one simple.

    def testDaemon(self):
        try:
            freeport=Pyro.socketutil.findUnusedPort()
            d=Pyro.core.Daemon(port=freeport)
            locationstr="%s:%d" %(Pyro.config.HOST, freeport)
            self.assertEqual( locationstr, d.locationStr)
            self.assertTrue(Pyro.constants.DAEMON_NAME in d.objectsById)
            self.assertEqual("PYRO:"+Pyro.constants.DAEMON_NAME+"@"+locationstr, str(d.uriFor(Pyro.constants.DAEMON_NAME)))
            self.assertTrue(d.fileno() > 0)
        finally:
            d.close()
        
    def testRegisterEtc(self):
        try:
            freeport=Pyro.socketutil.findUnusedPort()
            d=Pyro.core.Daemon(port=freeport)
            self.assertEquals(1, len(d.objectsById))
            o1=MyObj("object1")
            o2=MyObj("object2")
            d.register(o1)
            self.assertRaises(DaemonError, d.register, o2, Pyro.constants.DAEMON_NAME)  # cannot use daemon name
            self.assertRaises(DaemonError, d.register, o1, None)  # cannot register twice
            self.assertRaises(DaemonError, d.register, o1, "obj1a")
            d.register(o2, "obj2a")
            self.assertRaises(DaemonError, d.register, o2, "obj2b")
            
            self.assertEqual(3, len(d.objectsById))
            self.assertEquals(o1, d.objectsById[o1._pyroObjectId])
            self.assertEquals(o2, d.objectsById["obj2a"])
    
            # test unregister
            d.unregister("unexisting_thingie")
            d.unregister(None)
            d.unregister("obj2a")
            d.unregister(o1._pyroObjectId)
            self.assertEqual(1, len(d.objectsById))
            self.assertTrue(o1._pyroObjectId not in d.objectsById)
            self.assertTrue(o2._pyroObjectId not in d.objectsById)
        finally:
            d.close()

    def testDaemonObject(self):
        with Pyro.core.Daemon(port=0) as d:
            daemon=Pyro.core.DaemonObject(d)
            obj1=MyObj("object1")
            obj2=MyObj("object2")
            obj3=MyObj("object2")
            d.register(obj1,"obj1")
            d.register(obj2,"obj2")
            d.register(obj3)
            daemon.ping()
            registered=daemon.registered()
            self.assertTrue(type(registered) is list)
            self.assertEqual(4, len(registered))
            self.assertTrue("obj1" in registered)
            self.assertTrue("obj2" in registered)
            self.assertTrue(obj3._pyroObjectId in registered)
        
    def testUriFor(self):
        try:
            freeport=Pyro.socketutil.findUnusedPort()
            d=Pyro.core.Daemon(port=freeport)
            locationstr="%s:%d" %(Pyro.config.HOST, freeport)
            o1=MyObj("object1")
            o2=MyObj("object2")
            self.assertRaises(DaemonError, d.uriFor, o1)
            self.assertRaises(DaemonError, d.uriFor, o2)
            d.register(o1,None)
            d.register(o2,"object_two")
            o3=MyObj("object3")
            self.assertRaises(DaemonError, d.uriFor, o3)  #can't get an uri for an unregistered object (note: unregistered name is allright)
            u1=d.uriFor(o1)
            u2=d.uriFor(o2._pyroObjectId)
            u3=d.uriFor("unexisting_thingie")  # unregistered name is no problem, it's just an uri we're requesting
            u4=d.uriFor(o2)
            self.assertEquals(Pyro.core.PyroURI, type(u1))
            self.assertEquals("PYRO",u1.protocol)
            self.assertEquals("PYRO",u2.protocol)
            self.assertEquals("PYRO",u3.protocol)
            self.assertEquals("PYRO",u4.protocol)
            self.assertEquals("object_two",u4.object)
            self.assertEquals(Pyro.core.PyroURI("PYRO:unexisting_thingie@"+locationstr), u3)
        finally:
            d.close()
    
    def testDaemonWithStmt(self):
        d=Pyro.core.Daemon()
        self.assertTrue(d.transportServer is not None)
        d.close()   # closes the transportserver and sets it to None
        self.assertTrue(d.transportServer is None)
        with Pyro.core.Daemon() as d:
            self.assertTrue(d.transportServer is not None)
            pass
        self.assertTrue(d.transportServer is None)
        try:
            with Pyro.core.Daemon() as d:
                print 1//0 # cause an error
            self.fail("expected error")
        except ZeroDivisionError: 
            pass
        self.assertTrue(d.transportServer is None)
        d=Pyro.core.Daemon()
        with d:
            pass
        try:
            with d:
                pass
            self.fail("expected error")
        except PyroError:
            # you cannot re-use a daemon object in multiple with statements
            pass
        d.close()

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
