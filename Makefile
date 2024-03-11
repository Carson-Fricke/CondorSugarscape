CONFIG = config.json
DATACHECK = data/data.complete
PLOTCHECK = plots/plots.complete

CLEAN = *.json.conf \
		*.json.sslog \
		*.clog \
		*.log \
		*.pickle \
		*.submit \
		python3

LEAN = *.json.conf \
		*.clog \
		*.submit \
		*.pickle

# Change to python3 (or other alias) if needed
PYTHON = python3

setup:
	cp $(shell which python3 | head -n 1) .
	python3 codegen.py $(CONFIG)

condor:
	$(PYTHON) condor.py $(CONFIG)

run:
	$(PYTHON) condor.py $(CONFIG)

small:
	$(PYTHON) condor.py config-small.json

clean:
	rm -rf $(CLEAN) || true
	condor_rm $(shell whoami)

lean:
	rm -rf $(LEAN) || true
	condor_rm $(shell whoami)


# vim: set noexpandtab tabstop=4:
