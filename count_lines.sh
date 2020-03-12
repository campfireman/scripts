#! /bin/bash

if [ -z "$1" ]
then
	echo "file extension not set";
	exit 1;
fi

pipenv install $1 && pipenv lock -r > requirements.txt
