import unittest

import Pyro.util
import sys

def crash(arg=100):
    pre1="black"
    pre2=999
    def nest(p1,p2):
        s="white"+pre1
        x=pre2
        y=arg/2
        p3=p1/p2
        return p3
    a=10
    b=0
    s="hello"
    c=nest(a,b)
    return c

class TestUtils(unittest.TestCase):

    def testFormatTraceback(self):
        try:
            crash()
        except:
            tb="".join(Pyro.util.formatTraceback(detailed=False))
            self.assertTrue("p3=p1/p2" in tb)
            self.assertTrue("ZeroDivisionError" in tb)
            self.assertFalse(" a = 10" in tb)
            self.assertFalse(" s = 'whiteblack'" in tb)
            self.assertFalse(" pre2 = 999" in tb)
            self.assertFalse(" x = 999" in tb)
        try:
            crash()
        except:
            tb="".join(Pyro.util.formatTraceback(detailed=True))
            self.assertTrue("p3=p1/p2" in tb)
            self.assertTrue("ZeroDivisionError" in tb)
            self.assertTrue(" a = 10" in tb)
            self.assertTrue(" s = 'whiteblack'" in tb)
            self.assertTrue(" pre2 = 999" in tb)
            self.assertTrue(" x = 999" in tb)


    def testPyroTraceback(self):
        try:
            crash()
        except:
            pyro_tb=Pyro.util.formatTraceback(detailed=True)
        try:
            crash("stringvalue")
        except Exception,x: 
            setattr(x, Pyro.constants.TRACEBACK_ATTRIBUTE, pyro_tb)
            pyrotb="".join(Pyro.util.getPyroTraceback())
            self.assertTrue("crash(\"stringvalue\")" in pyrotb)
            self.assertTrue("TypeError:" in pyrotb)
            self.assertTrue("Remote traceback" in pyrotb)
            self.assertTrue("ZeroDivisionError" in pyrotb)
            
   
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()