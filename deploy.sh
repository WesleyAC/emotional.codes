#!/bin/sh

if [ -n "$(git status --porcelain)" ]; then
	echo "Working directory not clean, exiting!"
	exit 1
fi

git branch -D deploy
git checkout -b deploy
python3 main.py
find . | grep -v "^./out" | grep -v "^./.git" | xargs rm -rf
mv out/* .
rmdir out
git add .
git commit -m "Automatic deploy"
git push origin deploy
git checkout -
