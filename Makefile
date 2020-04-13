types:
	mypy --disallow-untyped-defs *.py

format:
	black **/*.py *.py

t:
	# python -m  pytest tests/*
	python -m  pytest tests/* -s
