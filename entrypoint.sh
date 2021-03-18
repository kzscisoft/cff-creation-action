#!/usr/bin/bash

REMOTE_URL="https://github.com/${GITHUB_REPOSITORY}"
COMMIT_URL="https://${GITHUB_ACTOR}:${INPUT_GITHUB_TOKEN}@github.com/${REPOSITORY}.git"

git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"
git config --global user.name "github-actions[bot]"

if [ -z ${INPUT_BRANCH} ]
then
    INPUT_BRANCH=${GITHUB_REF}
fi

if [ -z ${INPUT_GITHUB_TOKEN} ]
then
    echo 'No GitHub Token given, you can use "${{ secrets.GITHUB_TOKEN }}".'
    exit 1
fi

gen-cff --repo-url ${REMOTE_URL} $@

if [ -f "CITATION.cff" ]
then
    echo "Failed to create CITATION.cff file."
    exit 1
fi

git add CITATION.cff
git commit -m "CITATION File Generated - $(date)"
git push "${COMMIT_URL}" HEAD:${INPUT_BRANCH}