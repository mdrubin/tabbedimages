Our application uses icons from http://www.glyfx.com/products/free.html

These are free, but we're not permitted to distribute them as image files.

Luckily Seo has implemented a way of pickling serializable .NET objects, using 
cPickle (which is built in to IronPython).

The pickle file you need (included here) is from :

http://fepy.svn.sourceforge.net/viewvc/fepy/trunk/fepy/pickle.py?view=markup

In order to pickle .NET objects, their type must first be registered using
``fepy_pickle.register(type)``.

This file is *not* needed for unpickling files.

The file 'pickleImage.py' here, loads an image ('fuzzyman-m+m.jpg') as a .NET 
bitmap.

It then pickles it into a string, which it saves as a text file.

It then loads the image from the pickle and displays it in a PictureBox - just 
to prove that the image survives the pickling and unpickling process.