types:
	mypy --disallow-untyped-defs *.py

format:
	black **/*.py *.py

t:
	BLOCK_TWITCH_MSGS=true python -m pytest tests/*

f:
	BLOCK_TWITCH_MSGS=true python -m pytest tests/* -m focus
