The goal is to use (among others) the Python bottle library, to offer on the
one hand an API specific to the site http://dblp.uni-trier.de/db/ht/, which includes
the set of scientific publications in computer science, and on the other hand a website that makes it possible to use the previous API.
The DBLP site offers all the publications in the form of a file in XML format.

The first major point that posed a problem is the consequent size of the xml file made available to us (3GB) 
which prevents me from restarting the analysis of the file at every request.
It was necessary to carry out a pre-processing by coding a program allowing to generate several lighter subfiles. 
For this, my code divides the xml file into subfiles containing a specific number of posts. 
Using tags contained in the xml file, I was able to count them and set the number of publications per file, so ended up with 11 xml files of size around 250 MB.
