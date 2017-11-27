VERSION=$(shell python setup.py --version)

all:
	@echo
	@echo "version:" $(VERSION) $(DESCRIBE)
	@echo
	@echo "options:"
	@grep "^\S*:" ./Makefile | sed -e "s/^\(.*\):.*$$/  \1/g"
	@echo

run:
	./gvjinja.py -m gvjinja gvjinja.env |\
		tee gvjinja.gv | dot -T png > gvjinja.png
	./gvjinja.py -m gvjinja gvjinja.env -b |\
		tee gvjinja-basic.gv | dot -T png > gvjinja-basic.png

unittest:
	python -m unittest setup.suite

coverage:
	python -m coverage erase && \
	python -m coverage run setup.py && \
	python -m coverage report --include=gvjinja.py -m

develop:
	python setup.py develop

install: distclean
	python setup.py sdist && \
	pip install ./dist/gvjinja-$(VERSION).tar.gz

uninstall:
	pip uninstall gvjinja

distclean:
	\rm -fr __pycache__
	\rm -fr gvjinja.egg-info
	\rm -fr build dist

clean: distclean
	\rm -fr *~ *.pyc
