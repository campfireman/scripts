#!/bin/zsh

# arguments
PATTERN=$1
shift
DIRECTORIES=${@}

function print_usage() {
cat << EOF

SYNOPSIS:
	${0} PATTERN [DIRECTORY ...]

DESCRIPTION:
	Recurses into given directories and searches for a given pattern
	within those files. Selected file and line are then opened with
	default editor.

ARGUMENTS:
	PATTERN is used by grep with argument -i, thus case is ignored
	If DIRECTORY is not set the current path is selected as search path
	
EOF
}

if [ -z "${PATTERN}" ]; then
	print_usage
	exit 1
fi

echo ${DIRECTORIES}
if [ -z "${DIRECTORIES}" ]; then
	DIRECTORIES="./"
fi

SELECTED_FILE=$(grep -irn "${PATTERN}" ${DIRECTORIES} 2> /dev/null | sk)
SELECTED_FILE_PATH=$(echo "${SELECTED_FILE}" | grep -Po '^[^:]*')
SELECTED_FILE_LINE=$(echo "${SELECTED_FILE}" | grep -Po '(?<=:)[[:digit:]]+(?=:)')

if [ -z "${SELECTED_FILE_PATH}" ]; then
	echo "No matches."
	exit 0
fi

${EDITOR} "${SELECTED_FILE_PATH}" -c ":${SELECTED_FILE_LINE}"
echo "${EDITOR} ${SELECTED_FILE_PATH} -c :${SELECTED_FILE_LINE}" >> ${HOME}/.zhistory
