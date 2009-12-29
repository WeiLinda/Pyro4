import Pyro.naming

def handleCommand(ns, options, args):
    def printListResult(resultdict, title=""):
        print "--------START LIST",title
        for name,uri in sorted(resultdict.items()):
            print "%s --> %s" % (name, uri)
        print "--------END LIST",title
    def cmd_ping():
        ns.ping
        print "Name server ping ok."
    def cmd_listprefix():
        if len(args)==1:
            printListResult(ns.list())
        else:
            printListResult(ns.list(prefix=args[1]), "- prefix '%s'" % args[1])
    def cmd_listregex():
        if len(args)<2:
            raise SystemExit("missing regex argument")
        printListResult(ns.list(regex=args[1]), "- regex '%s'" % args[1])
    def cmd_register():
        ns.register(args[1], args[2])
        print "Registered",args[1]
    def cmd_remove():
        ns.remove(args[1])
        print "Removed",args[1]
        
    commands={
        "ping": cmd_ping,
        "list": cmd_listprefix,
        "listregex": cmd_listregex,
        "register": cmd_register,
        "remove": cmd_remove        
    }
    try:
        commands[args[0]]()
    except Exception,x:
        print "Error:",x
    
def main(args):
    from optparse import OptionParser
    parser=OptionParser()
    usage = """usage: %prog [options] command [arguments]\nCommand is one of: register remove list listregex ping"""
    parser = OptionParser(usage=usage)
    parser.add_option("-n","--host", dest="host", help="hostname of the NS")
    parser.add_option("-p","--port", dest="port", type="int", help="port of the NS")
    parser.add_option("-v","--verbose", action="store_true", dest="verbose", help="verbose output")
    options,args = parser.parse_args(args)    
    if not args or args[0] not in ("register","remove","list","listprefix", "listregex", "ping"):
        parser.error("invalid or missing command")
    if options.verbose:
        print "Locating name server..."
    ns=Pyro.naming.locateNS(options.host,options.port)
    if options.verbose:
        print "Name server found:",ns._pyroUri
    handleCommand(ns, options, args)
    if options.verbose:
        print "Done."

if __name__=="__main__":
    import sys
    main(sys.argv[1:])
