COVERAGE=coverage
PYTHON=python3
SOURCE_DATE_EPOCH=0
export SOURCE_DATE_EPOCH

all: build

build:
	flit build --no-use-vcs

check: test

clean:
	find . -not -path '*/.git/*' \
		\( -name '*.py[cdo]' -o -name '*.err' -o \
		-name '*,cover' -o -name __pycache__ \) -prune \
		-exec rm -rf '{}' ';'
	rm -rf dist build htmlcov
	rm -f .coverage cram.xml

dist:
	flit build --no-use-vcs --format sdist

install:
	flit install

quicktest:
	PYTHON=$(PYTHON) PYTHONPATH=`pwd` $(PYTHON) -m cram $(TESTOPTS) tests

test:
	$(COVERAGE) erase
	COVERAGE=$(COVERAGE) PYTHON=$(PYTHON) PYTHONPATH=`pwd` \
		$(PYTHON) -m cram $(TESTOPTS) tests
	$(COVERAGE) report --fail-under=100

.PHONY: all build check clean install dist quicktest test
