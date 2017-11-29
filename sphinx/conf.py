# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import sys, os
sys.path.insert(0,os.path.abspath(os.path.pardir))
import gvjinja

# sphinx extension module globs
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    ]

source_suffix = ['.rst',]
master_doc = 'index'
project = 'gvjinja'
copyright = '2017, Victor Hui'
author = 'Victor Hui'
version = gvjinja.__version__
release = gvjinja.__version__
add_module_names = False
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
html_theme = 'alabaster'
html_static_path = ['_static']
html_sidebars = {'**':[]}
