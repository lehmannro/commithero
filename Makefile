O ?=
VIRTUALENV = var

.PHONY: run clean
VIRTUAL = . "$(VIRTUALENV)/bin/activate";

run: $(VIRTUALENV)
	$(VIRTUAL) python setup.py install
	$(VIRTUAL) pip install dulwich
	$(VIRTUAL) commithero $(O) .

$(VIRTUALENV):
	virtualenv --distribute --no-site-packages "$(VIRTUALENV)"

clean:
	rm -rf "$(VIRTUALENV)" build/ dist/ CommitHero.egg-info/
	rm -f .commithero
