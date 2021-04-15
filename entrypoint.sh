#!/usr/bin/bash

if [ -n ${INPUT_REPOSITORY} ]
then
    INPUT_REPOSITORY=${GITHUB_REPOSITORY}
fi

REMOTE_URL="https://github.com/${GITHUB_REPOSITORY}"
COMMIT_URL="https://${GITHUB_ACTOR}:${INPUT_GITHUB_TOKEN}@github.com/${INPUT_REPOSITORY}.git"

git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"
git config --global user.name "github-actions[bot]"

ARGUMENTS=("--repo-url='${REMOTE_URL}'")

if [ -n "${INPUT_BRANCH}" ]
then
    INPUT_BRANCH=${GITHUB_REF}
fi

if [ ! -n "${INPUT_GITHUB_TOKEN}" ]
then
    echo 'No GitHub Token given, you can use "${{ secrets.GITHUB_TOKEN }}".'
    exit 1
fi

if [ -n "${INPUT_DOI}" ]
then
    ARGUMENTS+=("--doi='${INPUT_DOI}'")
fi

if [ -n "${INPUT_TITLE}" ]
then
    ARGUMENTS+=("--title='${INPUT_TITLE}'")
fi

if [ -n "${INPUT_MESSAGE}" ]
then
    ARGUMENTS+=("--message='${INPUT_MESSAGE}'")
fi

if [ -n "${INPUT_AUTHORS}" ]
then
    ARGUMENTS+=("--authors='${INPUT_AUTHORS}'")
fi

if [ -n "${INPUT_LANGUAGE}" ]
then
    ARGUMENTS+=("--language='${INPUT_LANGUAGE}'")
fi

if [ -n "${INPUT_AFFILIATION}" ]
then
    ARGUMENTS+=("--affiliation='${INPUT_AFFILIATION}'")
fi

gen-cff ${INPUT_PROJECT_PATH} "${ARGUMENTS[@]}"

if [ ! -f "CITATION.cff" ]
then
    echo "Failed to create CITATION.cff file."
    exit 1
fi

git add -f CITATION.cff
git commit -m "CITATION File Generated - $(date)"
git push "${COMMIT_URL}" HEAD:${INPUT_BRANCH}
