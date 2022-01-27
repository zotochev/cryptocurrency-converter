#!/bin/sh


if [ $# -eq 1 ]; then
	pipenv lock --keep-outdated --requirements > requirements.txt
	docker build -t cc_bot .
	docker run -d --rm -e "TOKEN=$1" --name cc_bot_cont cc_bot
else
	echo "Usage: sh start.sh <YOUR_TELEGRAM_TOKEN>"
fi
