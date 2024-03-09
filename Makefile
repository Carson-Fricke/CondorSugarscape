CONFIG = config.json
DATACHECK = data/data.complete
PLOTCHECK = plots/plots.complete

DATASET = $(DATACHECK) \
		data/*[[:digit:]]*.config \
		data/*.json \
		data/*.sh

PLOTS = $(PLOTCHECK) \
		plots/*.dat \
		plots/*.pdf \
		plots/*.plg

CLEAN = *.json.conf \
		*.json.sslog \
		*.clog \
		*.submit \
		python3 \
		$(DATASET) \
		$(PLOTS)

# Change to python3 (or other alias) if needed
PYTHON = python3
SUGARSCAPE = sugarscape.py
REMOTESUGARSCAPE = remote.py

# Check for local Bash and Python aliases
BASHCHECK = $(shell which bash > /dev/null; echo $$?)
PYCHECK = $(shell which python > /dev/null; echo $$?)
PY3CHECK = $(shell which python3 > /dev/null; echo $$?)

$(DATACHECK):
	cd data && $(PYTHON) run.py --conf ../$(CONFIG)
	touch $(DATACHECK)

$(PLOTCHECK): $(DATACHECK)
	cd plots && $(PYTHON) plot.py --path ../data/ --conf ../$(CONFIG) --outf data.dat
	touch $(PLOTCHECK)

all: $(DATACHECK) $(PLOTCHECK)

data: $(DATACHECK)

plots: $(PLOTCHECK)

seeds:
	cd data && $(PYTHON) run.py --conf ../$(CONFIG) --seeds

setup:
	cp $(shell which python3 | head -n 1) .
	python3 codegen.py $(CONFIG)

local:
	$(PYTHON) $(SUGARSCAPE) --conf $(CONFIG)

condor:
	$(PYTHON) condor.py $(CONFIG)

clean:
	rm -rf $(CLEAN) || true

lean:
	rm -rf $(PLOTS) || true

.PHONY: all clean data lean plots setup

# vim: set noexpandtab tabstop=4:
