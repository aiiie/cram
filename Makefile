COVERAGE=coverage
PYTHON=python3
SOURCE_DATE_EPOCH=0
export SOURCE_DATE_EPOCH

all: build

build:
	flit build --no-use-vcs

clean:
	find . -not -path '*/.git/*' \
		\( -name '*.err' -o -name '*,cover' -o -name __pycache__ \) -prune \
		-exec rm -rf '{}' ';'
	rm -rf .mypy_cache .ruff_cache .dist build htmlcov
	rm -f .coverage cram.xml

dist:
	flit build --no-use-vcs --format sdist

install:
	flit install

check: test

lint:
	ruff check
	ty check
	pyrefly check
	zuban check
	mypy .
	basedpyright

quicktest:
	PYTHON=$(PYTHON) $(PYTHON) -m cram $(TESTOPTS) tests

test:
	$(COVERAGE) erase
	COVERAGE=$(COVERAGE) PYTHON=$(PYTHON) $(PYTHON) -m cram $(TESTOPTS) tests
	$(COVERAGE) report --fail-under=100

testall:
	uv run --python=3.10 -m cram $(TESTOPTS) tests
	uv run --python=3.11 -m cram $(TESTOPTS) tests
	uv run --python=3.12 -m cram $(TESTOPTS) tests
	uv run --python=3.13 -m cram $(TESTOPTS) tests
	uv run --python=3.14 -m cram $(TESTOPTS) tests
	uv run --python=3.15 -m cram $(TESTOPTS) tests

.PHONY: all build clean dist install check lint quicktest test testall
