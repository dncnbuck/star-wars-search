python ?= python3

all: swsearch.egg-info build

swsearch.egg-info: setup.py build/.venv/bin/pip
	build/.venv/bin/pip install --process-dependency-links --upgrade --editable . && touch $@
build/.venv/bin/pip: build/.venv/bin/python
	build/.venv/bin/pip install --upgrade setuptools
	build/.venv/bin/python -m pip install pip==18.1
build/.venv/bin/python:
	$(python) -m venv build/.venv

build: requirements.txt
	build/.venv/bin/pip install -r requirements.txt && touch $@

test: all flake8 build/.venv/bin/coverage
	build/.venv/bin/coverage run -m pytest
build/.venv/bin/coverage: build/.venv/bin/pip
	build/.venv/bin/pip install coverage

flake8: build/.venv/bin/flake8
	build/.venv/bin/flake8 --max-line-length 120 swsearch
build/.venv/bin/flake8:
	build/.venv/bin/pip install flake8

clean:
	rm -rf .pytest_cache build .coverage
