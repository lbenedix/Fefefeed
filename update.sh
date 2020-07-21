#!/bin/bash

cd /home/lbenedix/Fefefeed

pipenv run get_items
pipenv run generate_feed

if $(git diff --stat | grep "1 insertion(+), 1 deletion(-)"); then
	echo "only one change"
#	git checkout feed.xml
else
	echo "real update"
#	git add .
#	git commit -m "new stuff"
#	git push
fi

