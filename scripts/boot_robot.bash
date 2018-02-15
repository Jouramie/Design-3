#!/usr/bin/env bash

# Set robot code to current commit

ACTUAL_BRANCH=$(git rev-parse --abbrev-ref HEAD)
echo ${ACTUAL_BRANCH}
git checkout -B robot
git remote add robot design3@10.42.0.1:~/robot
ssh design3@10.42.0.1 'cd ~/robot && git checkout --detach'
git push -f robot
ssh design3@10.42.0.1 'cd ~/robot && git checkout robot'
git checkout ${ACTUAL_BRANCH}


