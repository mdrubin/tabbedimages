#!C:\Python24\python.exe

# Author: Chris Liechti
# Contact: cliechti@gmx.net
# Revision: $Revision: 4156 $
# Date: $Date: 2005-12-08 05:43:13 +0100 (Thu, 08 Dec 2005) $
# Copyright: This module has been placed in the public domain.

"""
A minimal front end to the Docutils Publisher, producing HTML slides using
the S5 template system.
"""
import os
import sys
sys.path.insert(0, os.path.join(os.getcwd(), 'modules'))
import textmacros
import macros

from pythonutils import walkfiles, readfile, writefile

try:
    import locale
    locale.setlocale(locale.LC_ALL, '')
except:
    pass

from docutils.core import publish_cmdline, default_description


description = ('Generates S5 (X)HTML slideshow documents from standalone '
               'reStructuredText sources.  ' + default_description)

publish_cmdline(writer_name='s5', description=description)

if len(sys.argv) > 2:
    entry = sys.argv[2]
    body = readfile(entry)
    newbody = textmacros.replace_all(body, macros.__dict__, 1)
    writefile(entry, newbody)
