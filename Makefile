PYTHON ?= python3

.PHONY: check
check:
	$(PYTHON) scripts/check_project.py
