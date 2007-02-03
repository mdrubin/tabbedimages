# macros.py

# Subversion Details
# $LastChangedDate: 2005-05-28 12:14:08 +0100 (Sat, 28 May 2005) $
# $LastChangedBy: fuzzyman $
# $HeadURL: https://svn.rest2web.python-hosting.com/trunk/rest2web.py $
# $LastChangedRevision: 28 $

# macros for rest2web 
# http://www.voidspace.org.uk/python/rest2web

# Adapted from macros.py for Firedrop2 by Hans Nowak
# http://zephyrfalcon.org

# Copyright Michael Foord, 2004 & 2005.
# Released subject to the BSD License
# Please see http://www.voidspace.org.uk/python/license.shtml

# For information about bugfixes, updates, and support,
# please join the Pythonutils mailing list.
# http://groups.google.com/group/pythonutils/
# Comments, suggestions, and bug reports, welcome.
# Scripts maintained at http://www.voidspace.org.uk/python/index.shtml
# E-mail fuzzyman@voidspace.org.uk

# FIXME: Sort smiley stuff....
# XXXX
smiley_path, smiley_url = 'smilies', 'smilies/'


import cStringIO
import os
import sys
import traceback

    
##sys.__stdout__.write(os.getcwd())

# curlyl and curlyr is a way of including literal
# curly brackets in pages
curlyl = '{'
curlyr = '}'

cl = curlyl
cr = curlyr



def acronym(acronym, meaning=None):
    """
    Return the HTML for an acronym.
    """
    if meaning is None:
        # will raise a KeyError if the acronym isn't found
        meaning = acronyms[acronym.lower()] 
    return '<acronym title="%s">%s</acronym>' % (meaning, acronym)
acro = acronym

# a dictionary of standard acronyms
# keys should be lowercase
acronyms = {
    'wysiwyg': 'What You See Is What You Get',
    'html': 'HyperText Markup Language',
    'xml': 'eXtensible Markup Language',
    'xhtml': 'eXtensible HyperText Markup Language',
    'rest': 'ReStructuredText',
    'css': 'Cascading Style Sheets',
    'ie': 'Internet Exploder',
    'ide': 'Integrated Development Environment',
    'afaik': 'As Far as I Know',
    'ianal': 'I am not a Lawyer',
    'ssi': 'Server Side Includes',
    'cgi': 'Common Gateway Interface',
    'lol': 'Laughing Out Loud',
    'rotfl': 'Roll On the Floor Laughing',
    'http': 'HyperText Transfer Protocol',
    'ascii': 'American Standard Code for Information Interchange',
    'gui': 'Graphical User Interface',
    'cli': 'Command Line Interface',
    'pda': 'Personal Digital Assistant',
    'rtfm': 'Read the Manual',
    'ftp': 'File Transfer Protocol',
    'nntp': 'Network News Transfer Protocol',
    'uk': 'United Kingdom',
    'pc': 'Personal Computer',
    'url': 'Uniform Resource Locator',
    'uri': 'Uniform Resource Identifier',
    'tcp/ip': 'Transport Control Protocol/Internet Protocol',
    'udp': 'User Data Paragram',
    'yagni': 'You Aint Gonna Need It',
    }

def include(filename, escape='False'):
    """
    Include a file in the page.
    HTML only of course.
    """
    data = open(filename, 'r').read()
    if escape.lower() not in ['false', 'off', '0', 'no']:
        # FIXME: Should we check for invalid options and raise an error ?
        data = data.replace('\r\n', '\n')
        data = data.replace('\r', '\n')
        data = data.replace('\n', '<br />\n').replace('  ', '&nbsp;&nbsp;')
    return data
inc = include

try:
    import smiley as smiley_module
except ImportError:
    def smiley(text):
        """
        Attempting to use this without having the smiley module available
        will raise an ImportError.
        """
        raise ImportError, "Importing smiley.py failed."
#
else:
    smile = None
    def smiley(text):
        """
        Create a smiley.
        The smiley lib is only created on the first run through.
        """
        global smile
        if smile is None:
             smile = smiley_module.lib(smiley_path, smiley_url)
        s = smile.makehappy(' %s ' % text)
        s = s.replace('\n', '')
        return s.replace(' />', ' height="15" width="15" />')    # add the height
sm = smiley

#
# syntax coloring
try:
    import colorize as color
except ImportError:
    def colorize(filename):
        raise ImportError, 'Importing colorize.py failed.'
#
else:
    def colorize(filename):
        """
        format a python script as html
        Using the appropriate css it will be nicely colored.
        
        Needs the colorize.py module.
        """
        fullname = os.path.join(filename)
        f = open(fullname, 'r')
        data = f.read()
        f.close()
        #
        p = color.Parser(data)
        p.format(None, None)
        src = p.getvalue()
        return src.replace('\n', '<br />\n').replace('  ', '&nbsp;&nbsp;')
        # to avoid having to use <pre>..
col = colorize

class coloring:
    def open(self, data):
        p = color.Parser(data)
        p.format(None, None)
        src = p.getvalue()
        return src.replace('\n', '<br />\n').replace('  ', '&nbsp;&nbsp;')        
    
    def close(self, *args):
        pass

def name(n):
    return '<a name="%s" id="%s"></a>' % (n, n)

def title(text, size=3):
    """For titles of a named size"""
    return '<h%s>%s</h%s>' % (size, text, size)

def small(text):
    return '<small>%s</small>' % text



