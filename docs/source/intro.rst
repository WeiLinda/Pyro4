Intro and Example
*****************

This chapter contains a little overview of Pyro's features and a simple example to show how it looks like.

About Pyro
==========

Here's a quick overview of Pyro's features:

- written in 100% Python so extremely portable.
- support for all Python datatypes that are pickleable.
- runs on normal CPython 2.x, CPython 3.x, IronPython, Jython, Pypy.
- works between systems on different architectures and operating systems (64-bit, 32-bit, Intel, PowerPC...)
- designed to be very easy to use and get out of your way as much as possible.
- name server that keeps track of your object's actual locations so you can move them around transparently.
- support for automatic reconnection to servers in case of interruptions.
- automatic proxying of Pyro objects which means you can return references to remote objects just as if it were normal objects.
- one-way invocations for enhanced performance.
- batched invocations for greatly enhanced performance of many calls on the same object.
- you can define timeouts on network communications to prevent a call blocking forever if there's something wrong.
- asynchronous invocations if you want to get the results 'at some later moment in time'. Pyro will take care of gathering the result values in the background.
- remote exceptions will be raised in the caller, as if they were local. You can extract detailed remote traceback information.
- stable network communication code that works reliably on many platforms.
- possibility to use Pyro's own event loop, or integrate it into your own (or third party) event loop.
- many simple examples included to show various features and techniques.
- large amount of unit tests and high test coverage.
- built upon more than 10 years of existing Pyro history.


Pyro's history
^^^^^^^^^^^^^^
Little bit of history? (how Pyro came to be, Pyro 3, Pyro4)

Simple Example
==============

This example will show you in a nutshell what it's like to use Pyro in your programs.
A much more extensive introduction is found in the :doc:`tutorial`.

We're going to write a simple greeting service that will return a personalized greeting message to its callers.

Let's start by just writing it in normal Python first (create two files)::

    # save this as greeting.py
    class GreetingMaker(object):
        def get_fortune(self, name):
            return "Hello, {0}. Here is your fortune message:\n" \
                   "Behold the warranty -- the bold print giveth and the fine print taketh away.'".format(name)

    # save this as client.py
    import greeting
    name=raw_input("What is your name? ")
    greeting_maker=greeting.GreetingMaker()
    print greeting_maker.get_fortune(name)

If you then run it with :command:`python client.py` a session looks like this::

    $ python client.py
    What is your name? Irmen
    Hello, Irmen. Here is your fortune message:
    Behold the warranty -- the bold print giveth and the fine print taketh away.'

Right that works like a charm but we are now going to use Pyro to make this into a greeting server that you
can access easily from anywhere. The :file:`greeting.py` is going to be our server. We'll need to import the
Pyro package, start up a Pyro daemon (server) and connect a GreetingMaker object to it::

    # saved as greeting.py
    import Pyro4

    class GreetingMaker(object):
        def get_fortune(self, name):
            return "Hello, {0}. Here is your fortune message:\n" \
                   "Behold the warranty -- the bold print giveth and the fine print taketh away.'".format(name)

    greeting_maker=GreetingMaker()

    daemon=Pyro4.Daemon()                 # make a Pyro daemon
    uri=daemon.register(greeting_maker)   # register the greeting object as a Pyro object

    print "Ready. Object uri =", uri      # print the uri so we can use it in the client later
    daemon.requestLoop()                  # start the event loop of the server to wait for calls

And now all that is left is a tiny piece of code that invokes the server from somewhere::

    # saved as client.py
    import Pyro4

    uri=raw_input("What is the Pyro uri of the greeting object? ").strip()
    name=raw_input("What is your name? ").strip()

    greeting_maker=Pyro4.Proxy(uri)          # get a Pyro proxy to the greeting object
    print greeting_maker.get_fortune(name)   # call method normally

Open a console window and start the greeting server::

    $ python greeting.py
    Ready. Object uri = PYRO:obj_edb9e53007ce4713b371d0dc6a177955@localhost:51681

(The uri is randomly generated) Open another console window and start the client program::

    $ python client.py
    What is the Pyro uri of the greeting object?  <<paste the printed uri from the server>>
    What is your name?  <<type your name, Irmen in this example>>
    Hello, Irmen. Here is your fortune message:
    Behold the warranty -- the bold print giveth and the fine print taketh away.'

This covers the most basic use of Pyro! As you can see, all there is to it is starting a daemon,
registering one or more objects with it, and getting a proxy to these objects to call methods on
as if it was the actual object itself.

With a name server
^^^^^^^^^^^^^^^^^^
While the example above works, it could become tiresome to work with object uris like that.
There's already a big issue, *how is the client supposed to get the uri, if we're not copy-pasting it?*
Thankfully Pyro provides a *name server* that works like an automatic phonebook.
You can name your objects using logical names and use the name server to search for the
corresponding uri.

We'll have to modify a few lines in :file:`greeting.py` to make it register the object in the name server::

    # saved as greeting.py
    import Pyro4

    class GreetingMaker(object):
        def get_fortune(self, name):
            return "Hello, {0}. Here is your fortune message:\n" \
                   "Behold the warranty -- the bold print giveth and the fine print taketh away.'".format(name)

    greeting_maker=GreetingMaker()

    daemon=Pyro4.Daemon()                 # make a Pyro daemon
    ns=Pyro4.locateNS()                   # find the name server
    uri=daemon.register(greeting_maker)   # register the greeting object as a Pyro object
    ns.register("example.greeting", uri)  # register the object with a name in the name server

    print "Ready."
    daemon.requestLoop()                  # start the event loop of the server to wait for calls

The :file:`client.py` is actually simpler now because we can use the name server to find the object::

    # saved as client.py
    import Pyro4

    name=raw_input("What is your name? ").strip()

    greeting_maker=Pyro4.Proxy("PYRONAME:example.greeting")    # use name server object lookup uri shortcut
    print greeting_maker.get_fortune(name)

The program now needs a Pyro name server that is running. You can start one by typing the
following command: :command:`python -m Pyro4.naming` in a separate console window.
After that, start the server and client as before.
There's no need to copy-paste the object uri in the client any longer, it will 'discover'
the server automatically, based on the object name (:kbd:`example.greeting`).

This concludes this simple Pyro example.
