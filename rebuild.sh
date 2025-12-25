#!/bin/bash
source /opt/ros/humble/setup.bash
rm -rf build install log
colcon build --packages-select realsense_ros_gazebo
source install/setup.bash
ros2 launch realsense_ros_gazebo test_d435.launch.py