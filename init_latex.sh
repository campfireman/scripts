#!/bin/bash

if [ -f $1 ]; then
    echo "Please enter the name of the document";
    exit 1;
fi

NAME=$1
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
GITIGNORE_PATH="${SCRIPT_DIR}/gitignore_latex.txt"

mkdir -p "${NAME}/figures";
touch "${NAME}/${NAME}.tex"
touch "${NAME}/ref.bib"
code "${NAME}"
cp "${GITIGNORE_PATH}" "${NAME}/.gitignore"
