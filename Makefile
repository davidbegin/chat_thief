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
	cp db/sfx_votes.json db/backups/sfx_votes.json

restore:
	cp db/backups/users.json db/users.json
	cp db/backups/commands.json db/commands.json
	cp db/backups/issues.json db/issues.json
	cp db/backups/sfx_votes.json db/sfx_votes.json

# TODO: Move log files from the day before
new_day: backup
	rm db/play_soundeffects.json
	rm db/notifications.json
	rm db/cube_bets.json
	rm db/breaking_news.json
	rm db/votes.json
	rm .welcome

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

full_deploy: deploy_all


rename:
	sed -i 's/from chat_thief.soundeffects_library/from chat_thief.audioworld.soundeffects_library/' tests/**/*.py
	sed -i 's/from chat_thief.soundeffects_library/from chat_thief.audioworld.soundeffects_library/' chat_thief/**/*.py

	sed -i 's/from chat_thief.audio_player/from chat_thief.audioworld.audio_player/' tests/**/*.py
	sed -i 's/from chat_thief.audio_player/from chat_thief.audioworld.audio_player/' chat_thief/**/*.py

	sed -i 's/from chat_thief.sample_saver/from chat_thief.audioworld.sample_saver/' tests/**/*.py tests/*.py
	sed -i 's/from chat_thief.sample_saver/from chat_thief.audioworld.sample_saver/' tests/*.py
	sed -i 's/from chat_thief.sample_saver/from chat_thief.audioworld.sample_saver/' chat_thief/**/*.py chat_thief/*.py

	sed -i 's/from chat_thief.request_saver/from chat_thief.audioworld.request_saver/' tests/**/*.py tests/*.py
	sed -i 's/from chat_thief.request_saver/from chat_thief.audioworld.request_saver/' chat_thief/**/*.py chat_thief/*.py
