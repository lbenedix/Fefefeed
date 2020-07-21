#!/bin/bash

cd /home/lbenedix/Fefefeed

pipenv run get_items
pipenv run generate_feed

git diff --stat | grep feed.xml | grep "2 +-"
if [ $? -eq 0 ]; then
	echo OK, nothing new
	git checkout feed.xml
else
	echo "real update"
	git add .
	git commit -m "new stuff"
	git push
fi

