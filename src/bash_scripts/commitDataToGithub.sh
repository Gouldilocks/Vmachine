#!/bin/bash
./movecsvFiles.sh
# add files from above directory
git add ../resources/localStorage/VM_TEAMS.csv
git add ../resources/localStorage/VM_ITEMS.csv
git add ../resources/localStorage/VM_LOGS.csv
#commit with standard commit message
git commit -m "update VM_TEAMS.csv and VM_USERS.csv files"
# push changes to github
git push
