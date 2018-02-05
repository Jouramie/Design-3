#! /usr/bin/bash

# Update robot
git remote add robot design3@10.42.0.1:~/robot
git checkout robot
git push robot
git checkout master


# TODO start python script on the robot
