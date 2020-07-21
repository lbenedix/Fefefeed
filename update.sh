#!/bin/bash

cd /home/lbenedix/Fefefeed

pipenv run get_items
pipenv run generate_feed

if $(git diff --stat | grep "1 insertion(+), 1 deletion(-)"); then
	git checkout feed.xml
else
	git add .
	git commit -m "new stuff"
	git push
fi

