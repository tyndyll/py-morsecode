.. MorseCode documentation master file, created by
   sphinx-quickstart on Tue Nov 26 16:14:19 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Introduction
============

``morse`` is a Python package to generate Morse Code tones from Python code. "Morse code is 
a method of transmitting text information as a series of on-off tones, lights, or clicks that 
can be directly understood by a skilled listener or observer without special equipment" (from
http://en.wikipedia.org/wiki/Morse_Code). 

It consists of the following main modules:

* ``morse.code``: This is the primary library for generaing tones. Using this module
  provides access to a writer and an audio object

* ``morse.alphabet``: This library lists the available alphabets which can be used to 
  generate the output tones. Currently the only alphabet available is the "International"
  alphabet

Documentation
=============

.. toctree::
   :maxdepth: 2
   :numbered:

   morse.rst
   changes.rst

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
