#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$SCRIPT_DIR" || exit 1

curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o ros-archive-keyring.gpg

docker build -t realsense_gazebo_classis_env:latest .

exit 0