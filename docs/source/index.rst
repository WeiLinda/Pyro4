.. Pyro documentation master file, created by
   sphinx-quickstart on Thu Jun 16 22:20:40 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Pyro - Python Remote Objects - |version|
========================================

What is Pyro?
-------------
It is a library that enables you to build applications in which
objects can talk to each other over the network, with minimal programming effort.
You can just use normal Python method calls, with almost every possible parameter
and return value type, and Pyro takes care of locating the right object on the right
computer to execute the method. It is designed to be very easy to use, and to 
generally stay out of your way. But it also provides a set of powerful features that
enables you to build distributed applications rapidly and effortlessly.
Pyro is written in 100% pure Python and therefore runs on many platforms and Python versions,
**including Python 3.x**.

Pyro is copyright © Irmen de Jong (irmen@razorvine.net | http://www.razorvine.net).

`Pyro homepage <http://irmen.home.xs4all.nl/pyro/>`_ | `Pyro on Python package index <http://pypi.python.org/pypi/Pyro4/>`_ |
`Pyro mailing list <http://lists.sourceforge.net/lists/listinfo/pyro-core>`_ | :doc:`licensedisclaimer`

.. warning::
 This manual is still being written. It is incomplete and may contain errors.
 For the time being it may be helpful to read the `Pyro 3 manual <http://packages.python.org/Pyro/>`_ as well.
 Also in the source archive there is a directory :file:`examples` that contains a truckload 
 of example programs that show the various features.

Contents
--------

.. toctree::
   :maxdepth: 2
   
   Introduction
   Tutorial
   Installation and configuration <config>
   Upgrading from Pyro 3 <upgrading>
   Other stuff <other>
   Socketserver API <socketserver>
   Running on alternative Python implementations <alternative>
   Change log <changelog>
   License and disclaimer <licensedisclaimer>


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

