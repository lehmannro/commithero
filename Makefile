O ?=
R ?= .
VIRTUALENV = var

.PHONY: install run test clean
VIRTUAL = . "$(VIRTUALENV)/bin/activate";

run: install
	$(VIRTUAL) commithero $(O) $(R)

help:
	@echo " install      Install to virtualenv \$$VIRTUALENV (default: ./var)"
	@echo " run          Run on repository \$$R with options \$$O."
	@echo " install-git  Install Git backend."
	@echo " install-hg   Install Mercurial backend."
	@echo " install-bzr  Install Bazaar backend."
	@echo " install-svn  Install Subversion backend."
	@echo " test         Run test suite."
	@echo " clean        Remove build files and cache."

test:
	$(VIRTUAL) python setup.py --quiet test --verbose

install: $(VIRTUALENV)
	$(VIRTUAL) python setup.py --quiet install
$(VIRTUALENV):
	virtualenv --distribute --no-site-packages "$(VIRTUALENV)"

install-git: install
	$(VIRTUAL) pip install dulwich
install-hg: install
	$(VIRTUAL) pip install mercurial
install-bzr: install
	$(VIRTUAL) pip install bzr
install-svn: install
	$(VIRTUAL) pip install subvertpy

clean:
	rm -rf "$(VIRTUALENV)" build/ dist/ CommitHero.egg-info/
	rm -f .commithero
