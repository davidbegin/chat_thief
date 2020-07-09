check: format mypy t

format:
	black chat_thief/*.py chat_thief/**/*.py *.py tests/**/*.py tests/*.py

t:
	TEST_MODE=true BLOCK_TWITCH_MSGS=true python -m pytest --cov=chat_thief tests/*

fast:
	TEST_MODE=true BLOCK_TWITCH_MSGS=true python -m pytest -x --last-failed tests/*

slow:
	TEST_MODE=true BLOCK_TWITCH_MSGS=true python -m pytest --cov=chat_thief --durations=10 tests/*

f:
	TEST_MODE=true BLOCK_TWITCH_MSGS=true python -m pytest tests/* -m focus -s

backup:
	cp db/users.json db/backups/users.json
	cp db/commands.json db/backups/commands.json
	cp db/issues.json db/backups/issues.json
	cp db/sfx_votes.json db/backups/sfx_votes.json

restore:
	cp db/backups/users.json db/users.json
	cp db/backups/commands.json db/commands.json
	cp db/backups/issues.json db/issues.json
	cp db/backups/sfx_votes.json db/sfx_votes.json

# TODO: Move log files from the day before
new_day: backup
	rm db/notifications.json
	rm db/cube_bets.json
	rm db/breaking_news.json
	rm db/votes.json
	rm .welcome
	rm db/play_soundeffects.json

sync:
	scripts/sync_html.sh | lolcat

beginworld_html:
	python -m chat_thief.mygeoangelfirespace.publisher | lolcat

deploy: beginworld_html sync sync_json sync_sounds invalidate_cdn

invalidate_cdn:
	aws cloudfront create-invalidation \
			--distribution-id E382OTJDHBFSJL \
			--paths "/*" "/**/*"

deploy_all:
	aws s3 sync ./build/beginworld_finance s3://beginworld.exchange-f27cf15

sync_json:
	aws s3 sync ./db/ s3://beginworld.exchange-f27cf15/db

sync_sounds:
	aws s3 sync --exclude "*" \
		--include "*.mp3"       \
		--include "*.wav"       \
		--include "*.m4a"       \
		--include "*.opus"      \
		"/home/begin/stream/Stream/Samples/" s3://beginworld.exchange-f27cf15/media
	aws s3 sync --exclude "*" \
		--include "*.mp3"       \
		--include "*.wav"       \
		--include "*.m4a"       \
		--include "*.opus"      \
		"/home/begin/stream/Stream/Samples/theme_songs/" s3://beginworld.exchange-f27cf15/media

full_deploy: beginworld_html deploy_all

register_bots:
	python -m chat_thief.scripts.register_bots

types:
	mypy chat_thief/chat_parsers/soundeffect_request_parser.py --disallow-untyped-defs

mypy:
	mypy chat_thief/**/*.py --warn-unused-ignores
