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
	$(RM) docs/source/releases

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
	cp -r docs/resources/releases docs/source
	$(VENV)/bin/sphinx-autobuild \
		--host $(shell ifconfig | grep "inet " | grep -v 127.0.0.1 | cut -d\  -f2) \
		--watch pyrogram --watch docs/resources \
		-b html "docs/source" "docs/build/html" -j auto

docs-live-full:
	make clean-docs
	cd compiler/docs && ../../$(PYTHON) compiler.py
	cp -r docs/resources/releases docs/source
	$(VENV)/bin/sphinx-autobuild \
		--host $(shell ifconfig | grep "inet " | grep -v 127.0.0.1 | cut -d\  -f2) \
		--watch pyrogram --watch docs/resources \
		-b html "docs/source" "docs/build/html" -j auto

docs:
	make clean-docs
	rm docs/html.tar.gz
	cd compiler/docs && ../../$(PYTHON) compiler.py
	cp -r docs/resources/releases docs/source
	$(VENV)/bin/sphinx-build -b html "docs/source" "docs/build/html" -j auto
	cd docs/scripts && ../../$(PYTHON) sitemap.py && mv sitemap.xml ../build/html
	cp docs/robots.txt docs/build/html
	tar zcf docs/html.tar.gz docs/build/html
	make clean-docs

build:
	make clean-build
	make clean-api
	$(PYTHON) setup.py sdist
	$(PYTHON) setup.py bdist_wheel