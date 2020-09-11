#! /bin/bash

REPOSITORY_NAME=${PWD##*/}

FULL_INIT=0
DEFAULT_FILES=".gitignore"
VISIBILITY="p"
REMOTE_VAR="origin"
GITLAB_URL="https://gitlab.com"
TOKEN="_zM-YLzDvHXNezGYcSZy"

# Loop through arguments and process them
for arg in "$@"
do
    case $arg in
        -f=*|--full=*)
        FULL_INIT=1
        REPOSITORY_NAME="${arg#*=}"
        shift
        ;;
        -p|--public)
	    VISIBILITY="P"
        shift 
        ;;
        *)
        OTHER_ARGUMENTS+=("$1")
        shift # Remove generic argument from processing
        ;;
    esac
done


if [ ${FULL_INIT} -eq 1 ]
then
	mkdir ${REPOSITORY_NAME} && cd ${REPOSITORY_NAME} && git init && touch ${DEFAULT_FILES} && cd ..;
else
    cd ..;
fi
echo "$REPOSITORY_NAME"
URL=$(glab repo create "${REPOSITORY_NAME}" -${VISIBILITY})
searchstring="Project created:  https://"
echo "Repository created!"

URL=git@"${URL#*$searchstring}".git
URL=$(echo "$URL" | sed '0,/\//s//:/')

cd ${REPOSITORY_NAME} && git remote add origin "$URL"

if [ ${FULL_INIT} -eq 1 ]
then
	git add ${DEFAULT_FILES} && git commit -m "init"
fi

git push --set-upstream origin master
