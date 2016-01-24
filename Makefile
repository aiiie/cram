COVERAGE=coverage
PYTHON=python

ifdef PREFIX
PREFIX_ARG=--prefix=$(PREFIX)
endif

all: build

build:
	$(PYTHON) setup.py build

check: test

checkdist:
	check-manifest

clean:
	-$(PYTHON) setup.py clean --all
	find . -not \( -path '*/.hg/*' -o -path '*/.git/*' \) \
		\( -name '*.py[cdo]' -o -name '*.err' -o \
		-name '*,cover' -o -name __pycache__ \) -prune \
		-exec rm -rf '{}' ';'
	rm -rf dist build htmlcov
	rm -f README.md MANIFEST .coverage cram.xml

install: build
	$(PYTHON) setup.py install $(PREFIX_ARG)

dist:
	TAR_OPTIONS="--owner=root --group=root --mode=u+w,go-w,a+rX-s" \
		$(PYTHON) setup.py -q sdist

test:
	PYTHON=$(PYTHON) PYTHONPATH=`pwd` scripts/cram $(TEST_ARGS) tests

tests: test

coverage:
	$(COVERAGE) erase
	COVERAGE=$(COVERAGE) PYTHON=$(PYTHON) PYTHONPATH=`pwd` scripts/cram \
		$(TEST_ARGS) tests
	$(COVERAGE) report --fail-under=100

markdown:
	pandoc -f rst -t markdown README.rst > README.md

.PHONY: all build checkdist clean install dist test tests coverage markdown
