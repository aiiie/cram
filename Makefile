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
	rm -rf dist build
	rm -f MANIFEST

install: build
	$(PYTHON) setup.py install $(PREFIX_ARG)

dist:
	TAR_OPTIONS="--owner=root --group=root --mode=u+w,go-w,a+rX-s" $(PYTHON) setup.py -q sdist

tests:
	$(PYTHON) setup.py -q test

.PHONY: all build clean install dist tests
