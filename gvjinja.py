#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

gvjinja
~~~~~~~

A jinja module to create Graphviz directed graphs as
UML diagrams for jinja templates environments.

:copyright: (c) 2017 by Victor Hui.
:licence: BSD, see LICENSE for more details.

"""

from __future__ import print_function
import sys
from jinja2 import meta, Environment, DictLoader
from jinja2.meta import nodes

__author__ = 'Victor Hui'
__copyright__ = 'Copyright (C) 2017, Victor Hui'
__license__ = 'BSD-3-Clause'
__version__ = '0.9b0'

class Symble(object):
    """Symbol table of an abstract syntax tree.

    """

    str_types = (str,)
    if sys.version_info[0] == 2:
        str_types += (unicode,)

    def __init__(self,ast,name=""):
        self.ast = ast
        self.env = ast.environment
        self.name = name
        self.find_all = self.ast.find_all

    @property
    def undefines(self):
        var = []
        try:
            var = meta.find_undeclared_variables(self.ast)
        except:
            exc_type,exc,traceback = sys.exc_info()
            print('Symble: find_undeclared_variables ....',file=sys.stderr)
            error = '{}, {}'.format(exc_type.__name__,exc.message)
            print('  {}: {}'.format(self.name,error),file=sys.stderr)
        return list(map('{}: undefined'.format,var))

    @property
    def blocks(self):
        return list(
            '{}: block'.format(block.name)
            for block in self.find_all(nodes.Block))

    @property
    def macros(self):
        return list(
            '{}({}): macro'.format(
                macro.name,",".join(arg.name for arg in macro.args))
            for macro in self.find_all(nodes.Macro))

    @property
    def filters(self):
        return list(set(
            '{}(): filter'.format(f.name)
            for f in self.find_all(nodes.Filter)
            if f.name not in self.env.filters))

    def getrefs(self,reftype):
        """yield a list of references for a reference type.

        lifted from :func:`jinja2.meta.find_referenced_templates` to
        perform searching for specific reference types; no report for
        dynamic inheritances or inclusions;

        """
        for node in self.find_all(reftype):
            if not isinstance(node.template,nodes.Const):
                if isinstance(node.template,(nodes.Tuple,nodes.List)):
                    for template_name in node.template.items:
                        if isinstance(template_name.value,self.str_types):
                            yield template_name.value
            elif isinstance(node.template.value,self.str_types):
                yield node.template.value
            elif isinstance(node,node.Include):
                if isinstance(node.template.value,(tuple,list)):
                    for template_name in node.template.value:
                        yield template_name

    @property
    def extends(self):
        return list(set(self.getrefs(nodes.Extends)))

    @property
    def includes(self):
        return list(set(self.getrefs(nodes.Include)))

    def getimportants(self,node):
        if 'target' in node.fields:
            return node.target
        if 'names' in node.fields:
            return ",".join(
                fn if isinstance(fn,self.str_types) else ' as '.join(fn)
                for fn in node.names)

    @property
    def imports(self):
        yields = []
        for node in self.find_all((nodes.Import,nodes.FromImport)):
            # notes: no multiple imports?
            if isinstance(node.template,nodes.Const):
                if isinstance(node.template.value,self.str_types):
                    yields.append((
                        node.template.value,
                        self.getimportants(node)))
        return yields

    def __repr__(self):
        return '<Symble object for ast {!r}>'.format(self.name)


def getsymbles(jinja_env,extensions=""):
    """return a list of :class`Symbles` of a :class:`jinja2.Environment`;

    """
    symbles = []
    for name in jinja_env.list_templates():
        if not name.endswith(extensions):
            continue
        sourcetuple = jinja_env.loader.get_source(jinja_env,name)
        try:
            ast = jinja_env.parse(sourcetuple)
        except:
            exc_type,exc,traceback = sys.exc_info()
            print('getsymbles: parse ....',file=sys.stderr)
            error = '{}, {}'.format(exc_type.__name__,exc.message)
            print('  {}: {}'.format(name,error),file=sys.stderr)
            continue
        symbles.append(Symble(ast,name))
    return symbles


class gvjinja(object):
    """Jinja to create a Graphviz directed graph of a jinja environment.

    :class:`gvjinja` has:

    * templates, a dictionary of template strings;
    * env, a jinja environment of the templates;

    :class:`gvjinja` renders a directed graph for itself as a test.
    The gvjinja templates were designed test itself.

    >>> symbles = getsymbles(gvjinja.env)
    >>> assert len(symbles) == len(gvjinja.templates)
    >>> set(map(repr,symbles)) == set([
    ...     "<Symble object for ast 'DIGRAPH'>",
    ...     "<Symble object for ast 'DIGRAPHBASIC'>",
    ...     "<Symble object for ast 'EDGES'>",
    ...     "<Symble object for ast 'EXTENDS'>",
    ...     "<Symble object for ast 'IMPORTS'>",
    ...     "<Symble object for ast 'INCLUDES'>",
    ...     "<Symble object for ast 'NODE'>",
    ...     "<Symble object for ast 'NODELABEL'>",
    ... ])
    True
    >>> gvjinja.digraph(gvjinja.env) == gvjinja.digraph(symbles)
    True
    >>> all(map(gvjinja.digraph(gvjinja.env).__contains__,
    ...     gvjinja.templates.keys()))
    True

    * :meth:`digraph`(env), classmethod to print UML of env with nodes;
      the diagram has edge labels showing the name of the imported macros;

    >>> 'nodelabel as label' in gvjinja.digraph(gvjinja.env)
    True

    .. figure:: gvjinja.png

       ..

       Figure: gvjinja templates directed graph

    * :meth:`digraphbasic`(env), classmethod to print a basic graph diagram;
      the basic diagram has no detail of the nodes and no edge labels;

    >>> 'nodelabel as label' in gvjinja.digraphbasic(gvjinja.env)
    False

    .. figure:: gvjinja-basic.png

       ..

       Figure: gvjinja templates basic directed graph

    * exception test cases

      >>> templates = dict(
      ...     UNDEF = '{{ range(1)|undef }}',
      ...     SYNTAX = '{{ }}')
      >>> testenv = Environment(loader=DictLoader(templates))

      * setting up redirection of stderr for the test cases:

        >>> from contextlib import contextmanager
        >>> @contextmanager
        ... def redirecterr():
        ...     stderr, sys.stderr = sys.stderr, sys.stdout
        ...     yield
        ...     sys.stderr = stderr

      * a case of undefined filter:

        >>> s = getsymbles(testenv,extensions="UNDEF")
        >>> s
        [<Symble object for ast 'UNDEF'>]
        >>> with redirecterr():
        ...     s[0].undefines
        Symble: find_undeclared_variables ....
          UNDEF: TemplateAssertionError, no filter named 'undef'
        []

      * syntax error:

        >>> with redirecterr():
        ...     s = getsymbles(testenv,extensions="SYNTAX")
        getsymbles: parse ....
          SYNTAX: TemplateSyntaxError, Expected an expression, got 'end of print statement'
        >>> s # parse failed, no symbles!
        []


    """

    templates = dict(

DIGRAPHBASIC = '''\
digraph "jinja_env" {

rankdir = BT

node [
  shape = "record", color = "#0f0000",
  fontname = "Courier",
  style = "filled", fillcolor = "#fffffc",
]

edge [
  color = "#0f0000",
  fontname = "Courier", fontcolor = "#007f00",
]

{%- block nodes %}
{% endblock -%}

{%- block edges %}
{% for symble in symbles -%}
{% include "EDGES" with context -%}
{% endfor -%}
{% endblock %}
}
''',

DIGRAPH = '''\
{% extends "DIGRAPHBASIC" -%}
{% set extended = True %}{# the extension identfier #}

{%- block nodes %}
{% for symble in symbles %}
{% include "NODE" %}
{% endfor %}
{%- endblock %}
''',

NODE = '''\
{% from "NODELABEL" import nodelabel as label -%}
"{{ symble.name }}" [
  URL = "{{ symble.url }}",
  tooltip = "{{ symble.tooltip }}",
  label = "{ {{ label(symble) }} }",
]
''',

NODELABEL = '''\
{% macro nodelabel(symble) -%}
{% set attributes = (symble.undefines + symble.blocks + [""])|join("\l") -%}
{% set operations = (symble.filters + symble.macros + [""])|join("\l") -%}
{{ (symble.name, attributes, operations)|join("|") }}
{%- endmacro %}
''',

EDGES = '''\
{%- include ["EXTENDS","INCLUDES","IMPORTS"] -%}{#- test include from list -#}
{%- include ("INCLUDES","IMPORTS") -%}
{%- include "IMPORTS" -%}
''',

EXTENDS = '''\
{%- for ref in symble.extends %}
"{{ ref }}" -> "{{ symble.name }}" [ arrowhead = empty ]
{%- endfor %}
''',

INCLUDES = '''\
{%- for ref in symble.includes %}
"{{ ref }}" -> "{{ symble.name }}" [ arrowhead = open ]
{%- endfor %}
''',

IMPORTS = '''\
{%- for ref,funcs in symble.imports %}
"{{ ref }}" -> "{{ symble.name }}" [ arrowhead = diamond
  {%- if extended -%}, label = " {{ funcs }} " {%- endif %} ]
{%- endfor %}
''',

    )

    env = Environment(loader=DictLoader(templates))

    @classmethod
    def digraph(my,symbles,extensions=""):
        if isinstance(symbles,Environment):
            symbles = getsymbles(symbles,extensions)
        return my.env.get_template('DIGRAPH').render(symbles=symbles)

    @classmethod
    def digraphbasic(my,symbles,extensions=""):
        if isinstance(symbles,Environment):
            symbles = getsymbles(symbles,extensions)
        return my.env.get_template('DIGRAPHBASIC').render(symbles=symbles)


if __name__ == '__main__':

    import os
    from importlib import import_module
    import doctest

    def run():
        """\
Usage:  gvjinja.py [-m [module] [env]] [-b]

# print usage;
$ gvjinja.py

# render a digraph of gvjinja itself;
$ gvjinja.py -m gvjinja gvjinja.env |\\
        tee gvjinja.gv | dot -T png > gvjinja.png

# render a basic digraph of gvjinja itself;
$ gvjinja.py -m gvjinja gvjinja.env -b |\\
        tee gvjinja-basic.gv | dot -T png > gvjinja-basic.png

"""
        if (len(sys.argv) == 1 or
            '-m' != sys.argv[1] or
            len(sys.argv) < 4):
            print(run.__doc__,file=sys.stderr)
            return

        env = import_module(sys.argv[2])
        for attr in sys.argv[3].split("."):
            env = getattr(env,attr)
        if not isinstance(env,Environment):
            raise TypeError(
                '{!r} is not a jinja environment!'.format(env_name))
        if '-b' in sys.argv:
            print(gvjinja.digraphbasic(env))
        else:
            print(gvjinja.digraph(env))


    if sys.argv[0] != "":
        run()
    else:
        testresults = doctest.testmod(
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE)
        print(testresults,file=sys.stderr)
        exec(doctest.script_from_examples(gvjinja.__doc__))
