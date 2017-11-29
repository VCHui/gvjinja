#!/usr/bin/env python
# -*- coding: utf-8 -*-
"gvjinja - create Graphviz directed graphs for jinja templates"

import sys, subprocess
import doctest
import unittest
from setuptools import setup
import gvjinja

assert __doc__
assert gvjinja.__author__ == 'Victor Hui'
assert gvjinja.__copyright__ == 'Copyright (C) 2017, Victor Hui'
assert gvjinja.__license__ == 'BSD-3-Clause'
assert gvjinja.__version__

url = 'https://github.com/vc-h/gvjinja'
download_url = url + '/' + gvjinja.__version__ + 'tar.gz'


def getversion():
    "return the pypi version convention of git describe"
    describes = subprocess.check_output('git describe --abbrev=1 HEAD'.split())
    describes = describes.decode().strip().split("-")
    if len(describes) == 1:
        return describes[0]
    return '.post'.join(describes[:-1])


def suite():
    "use for setup.test_suite."
    tests = unittest.TestSuite()
    tests.addTest(doctest.DocTestSuite(gvjinja))
    return tests


if __name__ == '__main__':

    if len(sys.argv) == 1:
        runner = unittest.TextTestRunner(verbosity=1,failfast=True)
        runner.run(suite())
    else:
        setup(
            name = 'gvjinja',
            version = getversion(),
            description = __doc__,
            long_description = gvjinja.__doc__,
            author = gvjinja.__author__,
            author_email = 'vc-h@users.noreply.github.com',
            license = gvjinja.__license__,
            url = url,
            download_url = download_url,
            platforms = 'any',
            install_requires = ['jinja2>2.0',],
            test_suite = 'setup.suite',
            py_modules = ['gvjinja',],
            scripts = ['gvjinja.py',],
            include_package_data = True,
            zip_safe = False, # True, but False makes pip uninstall possible
            classifiers = [
                'Topic :: Software Development :: Documentation',
                'Topic :: Text Processing :: Markup',
                'Environment :: Console',
                'Intended Audience :: Developers',
                'Operating System :: OS Independent',
                'Development Status :: 4 - Beta',
                'License :: OSI Approved :: BSD License',
                'Programming Language :: Python :: 2.7',
                'Programming Language :: Python :: 3.6',
                ],
            )
