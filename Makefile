PYTHON=python

ifdef PREFIX
PREFIX_ARG=--prefix=$(PREFIX)
endif

all: build

build:
	$(PYTHON) setup.py build

clean:
	-$(PYTHON) setup.py clean --all
	find . -name '*.py[cdo]' -exec rm -f '{}' ';'
	find . -name '*.err' -exec rm -f '{}' ';'
	rm -rf dist build htmlcov
	rm -f README.md MANIFEST *,cover .coverage

install: build
	$(PYTHON) setup.py install $(PREFIX_ARG)

dist:
	TAR_OPTIONS="--owner=root --group=root --mode=u+w,go-w,a+rX-s" \
	$(PYTHON) setup.py -q sdist

tests:
ifeq ($(PYTHON),all)
	python2.4 setup.py -q test
	python2.5 setup.py -q test
	python2.6 setup.py -q test
	python2.7 setup.py -q test
	python3.1 setup.py -q test
else
	$(PYTHON) setup.py -q test
endif

coverage:
	$(PYTHON) setup.py -q test --coverage && \
	coverage report && \
	coverage annotate

markdown:
	pandoc -f rst -t markdown README.txt > README.md

.PHONY: all build clean install dist tests coverage markdown
