# Makefile for Sphinx documentation
SPHINXBUILD   = python -msphinx
BUILDDIR      = _build

html:
	$(SPHINXBUILD) -b html -d $(BUILDDIR)/doctrees . $(BUILDDIR)/html

clean:
	rm -rf *~ $(BUILDDIR)/*
