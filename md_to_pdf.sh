#! /bin/bash

STYLE_DIR="/home/ture/lib/latex-styles"

if [ -f "ref.bib" ]; then
	ref="--filter citeproc --bibliography ref.bib --csl $STYLE_DIR/ieee.csl"
else
	ref=""
fi

if [ -f $STYLE_DIR"/defaults.yaml" ]; then
	defaults="--metadata-file $STYLE_DIR/defaults.yaml"
else
	defaults=""
fi

for file in *.md; do
	filename=$(basename -s .md $file)
	TEXINPUTS=$TEXINPUTS":$STYLE_DIR" pandoc --from markdown $ref $defaults $file -o $filename".pdf"
done
