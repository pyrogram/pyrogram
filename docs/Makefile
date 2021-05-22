# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    = -j $(shell nproc --all)
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = Pyrogram
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

lhtml: # live html
	sphinx-autobuild --host $(shell ifconfig | grep "inet " | grep -v 127.0.0.1 | cut -d\  -f2) -b html "$(SOURCEDIR)" "$(BUILDDIR)/html" $(SPHINXOPTS)
