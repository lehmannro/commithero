O ?=
R ?= .
VIRTUALENV = var

.PHONY: install run test clean
VIRTUAL = . "$(VIRTUALENV)/bin/activate";

run: install
	$(VIRTUAL) commithero $(O) $(R)

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
