#! /bin/bash

if [ -z "$1" ]
then
	echo "file extension not set";
	exit 1;
fi

find . -name "*$1" | xargs wc -l | sort -nr
