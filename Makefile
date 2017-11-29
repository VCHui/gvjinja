VERSION	= $(shell python setup.py --version)

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

checktest:
	python setup.py check
	python setup.py test

unittest:
	python -m unittest setup.suite

coverage:
	python -m coverage erase && \
	python -m coverage run setup.py && \
	python -m coverage report --include=gvjinja.py -m

setup_install: distclean
	python setup.py install

setup_install_develop: distclean
	python setup.py develop

pip_install_editable: distclean
	pip install --editable .

pip_install: distclean
	pip install .

uninstall:
	pip uninstall gvjinja

distclean:
	\rm -fr __pycache__
	\rm -fr gvjinja.egg-info
	\rm -fr build dist

clean: distclean
	\rm -fr *~ *.pyc

sphinx:
	sphinx-apidoc --maxdepth=1 --full --ext-autodoc -o ./sphinx .
