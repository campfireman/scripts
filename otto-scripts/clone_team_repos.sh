#! /bin/bash

# team id of black unicorns
TEAM_ID=3060907

for name in $(curl -H "Authorization: token ${GITHUB_PERSONAL_ACCESS_TOKEN}" -X GET "https://api.github.com/teams/${TEAM_ID}/repos?per_page=100" | jq -r ".[].full_name");
do
	git clone "git@github.com:$name.git"
done
