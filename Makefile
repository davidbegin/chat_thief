SHELL := /bin/bash

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

save_file="$$(date -u "+%Y-%m-%d").log"

save_logs:
	cp logs/chat.log "logs/${save_file}"

new_day: save_logs backup
	rm logs/chat.log
	rm .welcome
	rm db/notifications.json
	rm db/breaking_news.json
	rm db/play_soundeffects.json
	rm db/cube_bets.json

sync:
	scripts/sync_html.sh | lolcat

beginworld_html:
	python -m chat_thief.mygeoangelfirespace.publisher | lolcat

deploy: beginworld_html sync sync_json sync_sounds invalidate_cdn

invalidate_cdn:
	aws cloudfront create-invalidation \
			--distribution-id E382OTJDHBFSJL \
			--paths "/*" "/**/*"


pull_user:
	aws s3api get-object --bucket beginworld.exchange-f27cf15 --key beginbot.html bucket_beginworld.html

deploy_user: gen_user_page sync_user invalidate_cdn

gen_user_page:
	python -m chat_thief.mygeoangelfirespace.user_publisher -u $(USER)

sync_user:
	aws s3api put-object                                                        \
		--bucket beginworld.exchange-f27cf15                                      \
	 	--key $(USER).html                                                       \
		--body /home/begin/code/chat_thief/build/beginworld_finance/$(USER).html \
		--content-type "text/html"

sync_json:
	aws s3 sync ./db/ s3://beginworld.exchange-f27cf15/db

deploy_all:
	aws s3 sync ./build/beginworld_finance s3://beginworld.exchange-f27cf15

sync_sounds:
	aws s3 sync --exclude "*" \
		--include "*.mp3"       \
		--include "*.wav"       \
		--include "*.m4a"       \
		--include "*.opus"      \
		--include "*.ogg"      \
		"/home/begin/stream/Stream/Samples/" s3://beginworld.exchange-f27cf15/media
	aws s3 sync --exclude "*" \
		--include "*.mp3"       \
		--include "*.wav"       \
		--include "*.m4a"       \
		--include "*.opus"      \
		--include "*.ogg"      \
		"/home/begin/stream/Stream/Samples/theme_songs/" s3://beginworld.exchange-f27cf15/media

full_deploy: beginworld_html deploy_all

register_bots:
	python -m chat_thief.scripts.register_bots

types:
	mypy chat_thief/new_commands/new_cube_casino.py --disallow-untyped-defs | grep new_cube_casino
	# mypy chat_thief/routers/economy_router.py --disallow-untyped-defs | grep economy_router

mypy:
	mypy chat_thief/**/*.py --warn-unused-ignores --disallow-untyped-defs

audio_authorizer:
	 FLASK_APP=chat_thief/apps/audio_authorizer.py flask run -p 1989
