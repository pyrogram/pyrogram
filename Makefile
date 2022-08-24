VENV := venv
PYTHON := $(VENV)/bin/python

RM := rm -rf

.PHONY: venv build docs

venv:
	$(RM) $(VENV)
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install -U pip wheel setuptools
	$(PYTHON) -m pip install -U -r requirements.txt -r dev-requirements.txt -r docs/requirements.txt
	@echo "Created venv with $$($(PYTHON) --version)"

clean-build:
	$(RM) *.egg-info build dist

clean-docs:
	$(RM) docs/build
	$(RM) docs/source/api/bound-methods docs/source/api/methods docs/source/api/types docs/source/telegram

clean-api:
	$(RM) pyrogram/errors/exceptions pyrogram/raw/all.py pyrogram/raw/base pyrogram/raw/functions pyrogram/raw/types

clean:
	make clean-build
	make clean-docs
	make clean-api

api:
	cd compiler/api && ../../$(PYTHON) compiler.py
	cd compiler/errors && ../../$(PYTHON) compiler.py

docs-live:
	make clean-docs
	cd compiler/docs && ../../$(PYTHON) compiler.py
	$(RM) docs/source/telegram
	$(VENV)/bin/sphinx-autobuild \
		--host $(shell ifconfig | grep "inet " | grep -v 127.0.0.1 | cut -d\  -f2) \
		--watch pyrogram --watch docs/resources \
		-b html "docs/source" "docs/build/html" -j auto

docs-live-full:
	make clean-docs
	cd compiler/docs && ../../$(PYTHON) compiler.py
	$(VENV)/bin/sphinx-autobuild \
		--host $(shell ifconfig | grep "inet " | grep -v 127.0.0.1 | cut -d\  -f2) \
		--watch pyrogram --watch docs/resources \
		-b html "docs/source" "docs/build/html" -j auto

docs:
	make clean-docs
	cd compiler/docs && ../../$(PYTHON) compiler.py
	$(VENV)/bin/sphinx-build \
		-b html "docs/source" "docs/build/html" -j auto

build:
	make clean-build
	make clean-api
	$(PYTHON) setup.py sdist
	$(PYTHON) setup.py bdist_wheel