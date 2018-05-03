#!/bin/bash
# initialize parameters
# identify pull request and push
# prepare upload path, request url
echo "inside ff-start.sh script"

SCANTIST_IMPORT_URL="http://e8482e5c.ngrok.io/import/"

show_project_info() {
  echo "CIRCLE_BRANCH $CIRCLE_BRANCH"
  echo "CIRCLE_SHA1 $CIRCLE_SHA1"
  echo "CIRCLE_USERNAME $CIRCLE_USERNAME"
  echo "CIRCLE_REPOSITORY_URL $CIRCLE_REPOSITORY_URL"
  echo "CIRCLE_PR_REPONAME $CIRCLE_PR_REPONAME"
  echo "CI_PULL_REQUEST $CI_PULL_REQUEST"
  echo "CIRCLE_PROJECT_USERNAME $CIRCLE_PROJECT_USERNAME"
  echo "CIRCLE_PROJECT_REPONAME $CIRCLE_PROJECT_REPONAME"
  echo "=================project info====================="
}
echo "=================show_project_info================="
show_project_info

$repo_name=$CIRCLE_PROJECT_USERNAME"/"$CIRCLE_PROJECT_REPONAME
$commit_sha=$CIRCLE_SHA1

ls

cwd=$(pwd)
echo $cwd

pyenv versions

pyenv global 3.6.2

python TreeBuilder.py $cwd $repo_name $commit_sha

#Log that the script download is complete and proceeding
echo "Uploading report at $SCANTIST_IMPORT_URL"

#Log the curl version used
curl --version

curl -g -v -f -X POST -d '@dependency-tree.json' -H 'Content-Type:application/json' "$SCANTIST_IMPORT_URL"

#Exit with the curl command's output status
exit $?
