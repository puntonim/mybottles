# This Makefile requires the following commands to be available:
# * virtualenv
# * python

DEPS:=requirements.txt
VIRTUALENV=$(shell which virtualenv)
PIP:="venv/bin/pip"
CMD_FROM_VENV:=". venv/bin/activate; which"
PYTHON=$(shell "$(CMD_FROM_VENV)" "python3")

.PHONY: venv deploy/qa requirements pyclean clean pipclean killmanage serve shell tests tox test pytests pytest lint isort setup.py publish

venv:
	$(VIRTUALENV) -p $(shell which python3) venv
	. venv/bin/activate
	$(PIP) install -U "pip>=19.0" -q
	$(PIP) install -U -r $(DEPS)

_make_venv_if_empty:
	@[ -e ./venv/bin/python ] || make venv


## Utilities for the venv currently active.

_ensure_active_env:
ifndef VIRTUAL_ENV
	@echo 'Error: no virtual environment active'
	@exit 1
endif

requirements: _ensure_active_env
	pip install -U "pip>=19.0" -q
	pip install -U -r $(DEPS)


## Generic utilities.

pyclean:
	find . -name *.pyc -delete
	rm -rf *.egg-info build
	rm -rf coverage.xml .coverage
	rm -rf .pytest_cache
	rm -rf __pycache__

clean: pyclean
	rm -rf venv
	rm -rf .tox
	rm -rf dist

pipclean:
	rm -rf ~/Library/Caches/pip
	rm -rf ~/.cache/pip


## Django local dev in the venv currently active.

killmanage: _ensure_active_env
	# Prefix `-` to continue also in case of return code <> 0.
	#-pkill -f manage.py
	pkill -f manage.py

serve: _ensure_active_env
	python ./manage.py runserver

serveplus: _ensure_active_env
	python ./manage.py runserver_plus --nopin

shell: _ensure_active_env
	python ./manage.py shell

shellplus: _ensure_active_env
	python ./manage.py shell_plus

tests-dev: _ensure_active_env
	#python ./manage.py test
	pytest tests -s

test-dev/%: _ensure_active_env
	pytest tests -s -k $*

recreatedb-dev: _ensure_active_env
	scripts/recreatedbdev.sh


## Tests.

tests: clean venv
	pytest tests -s


## Linters.
## Without TOX.

lint: _make_venv_if_empty
	flake8 .

isort: _make_venv_if_empty
	isort -rc .

isort-check: _make_venv_if_empty
	isort -rc -c .
