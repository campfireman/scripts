#! /bin/bash

if [ -z "$1" ]
then
	echo "commit message is not set";
	exit 1;
fi

git add * && git commit -am "$1" && git push
