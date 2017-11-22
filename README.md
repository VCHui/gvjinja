# gvjinja
Create Graphviz graph files for templates of jinja environments

## Description
[`gvjinja.py`](https://github.com/VC-H/gvjinja/blob/master/gvjinja.py)
has a set of jinja templates to generate to `stdout` the Graphviz graph
file (the dot-language) for the templates of a jinja environment. Then,
`dot` of Graphviz creates the graphic output from the graph file.

## Installation requirements
* [jinja](https://github.com/pallets/jinja)
* [Graphviz](http://www.graphviz.org)
* shell environment

## Usage examples

* Command-line options
  ```shell
  python gvjinja.py [-m [module] [env]] [-b]
  ```
* Create the graph diagram for the templates of gvjinja itself
  ```shell
  python gvjinja.py -m gvjinja gvjinja.env | dot -T png > gvjinja.png
  ```
  ![digraph](https://github.com/VC-H/gvjinja/blob/master/gvjinja.png?raw=true)

* Create a basic graph diagram
  ```shell
  python gvjinja.py -m gvjinja gvjinja.env -b | dot -T png > gvjinja-basic.png
  ```
  ![digraph](https://github.com/VC-H/gvjinja/blob/master/gvjinja-basic.png?raw=true)

## Similar projects
* [jinja2gv](https://github.com/maxim-s-barabash/jinja2gv)
