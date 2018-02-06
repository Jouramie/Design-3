#! /usr/bin/bash

# Update robot
git remote add robot design3@10.42.0.1:~/robot
git checkout origin/robot
git push robot/robot
git checkout origin/master


# TODO start python script on the robot
