PYTHON=python

ifdef PREFIX
PREFIX_ARG=--prefix=$(PREFIX)
endif

all: build

build:
	$(PYTHON) setup.py build

clean:
	-$(PYTHON) setup.py clean --all
	find . -not -path '*/.hg/*' -name '*.py[cdo]' -exec rm -f '{}' ';'
	find . -name '*.err' -exec rm -f '{}' ';'
	rm -rf __pycache__ dist build htmlcov
	rm -f README.md MANIFEST *,cover .coverage

install: build
	$(PYTHON) setup.py install $(PREFIX_ARG)

dist:
	TAR_OPTIONS="--owner=root --group=root --mode=u+w,go-w,a+rX-s" \
	$(PYTHON) setup.py -q sdist

tests:
ifeq ($(PYTHON),all)
	python2.4 -tt setup.py -q test
	python2.5 -tt setup.py -q test
	python2.6 -tt -3 setup.py -q test
	python2.7 -tt -3 setup.py -q test
	python3.2 -tt -bb setup.py -q test
	python3.3 -tt -bb setup.py -q test
else
	$(PYTHON) -tt setup.py -q test
endif

coverage:
	$(PYTHON) setup.py -q test --coverage && \
	coverage report && \
	coverage annotate

# E261: two spaces before inline comment
# E301: expected blank line
# E302: two new lines between functions/etc.
pep8:
	pep8 --ignore=E125,E261,E301,E302 --repeat cram.py setup.py

pyflakes:
	pyflakes cram.py setup.py

pylint:
	pylint --rcfile=.pylintrc cram.py setup.py

markdown:
	pandoc -f rst -t markdown README.txt > README.md

.PHONY: all build clean install dist tests coverage pep8 pyflakes pylint \
	markdown
