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

clean:
	rm -rf "$(VIRTUALENV)" build/ dist/ CommitHero.egg-info/
	rm -f .commithero
