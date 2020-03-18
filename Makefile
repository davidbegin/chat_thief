types:
	mypy --disallow-untyped-defs *.py

format:
	black **/*.py *.py
