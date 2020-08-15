#! /bin/bash

if [ -z "$1" ]
then
	echo "bib file not set";
	exit 1;
fi

if [ -z "$2" ]
then
	echo "stylesheet not set";
	exit 1;
fi

if [ -z "$3" ]
then
	echo "metadata file not set";
	exit 1;
fi

if [ -z "$4" ]
then
	echo "input file not set";
	exit 1;
fi

if [ -z "$5" ]
then
	echo "ouput file not set";
	exit 1;
fi


TEXINPUTS=$TEXINPUTS":~/lib/latex-styles" pandoc --filter pandoc-citeproc  --from markdown --bibliography="$1"  --csl="$2" --metadata-file "$3" "$4" -o "$5"
