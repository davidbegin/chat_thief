types:
	mypy --disallow-untyped-defs *.py

format:
	black chat_thief/*.py chat_thief/**/*.py *.py
	black tests/**/*.py tests/*.py

t:
	TEST_MODE=true BLOCK_TWITCH_MSGS=true python -m pytest --cov=chat_thief tests/*

f:
	TEST_MODE=true BLOCK_TWITCH_MSGS=true python -m pytest tests/* -m focus -s

backup:
	cp db/users.json db/backups/users.json
	cp db/commands.json db/backups/commands.json
	cp db/issues.json db/backups/issues.json

restore:
	cp db/backups/users.json db/users.json
	cp db/backups/commands.json db/commands.json
	cp db/backups/issues.json db/issues.json
