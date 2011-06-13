from __future__ import print_function
import sys
import Pyro4

if sys.version_info<(3,0):
    input=raw_input


class Viewer(object):
    def quote(self, market, symbol, value):
        print("{0}.{1}: {2}".format(market, symbol, value))


def main():
    viewer=Viewer()
    daemon=Pyro4.Daemon()
    viewer_uri=daemon.register(viewer)
    agg=Pyro4.Proxy("PYRONAME:stockquote.aggregator")
    print("Available stock symbols:",agg.available_symbols())
    symbols=input("Enter symbols you want to view (comma separated):")
    symbols=[symbol.strip() for symbol in symbols.split(",")]
    agg.view(Pyro4.Proxy(viewer_uri), symbols)
    print("Viewer listening on symbols",symbols)
    daemon.requestLoop()

if __name__ == "__main__":
    main()
