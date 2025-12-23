FROM ros:humble-perception

ARG USERNAME=realsense
ARG UID=1000
ARG GID=$UID

ENV DEBIAN_FRONTEND=noninteractive

# 删除可能残留的 ROS2 软件源配置和 key
RUN rm -f /etc/apt/sources.list.d/ros2* \
    && rm -f /usr/share/keyrings/ros*.gpg

# 添加ROS2 GPG密钥和软件源
COPY ros-archive-keyring.gpg /usr/share/keyrings/ros-archive-keyring.gpg
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] https://mirrors.ustc.edu.cn/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" \
    > /etc/apt/sources.list.d/ros2.list

# 替换为中科大镜像源
RUN sed -i 's|http://.*.ubuntu.com|https://mirrors.ustc.edu.cn|g' /etc/apt/sources.list \
    && apt-get update

# ----------------------------
# Install dependencies
# ----------------------------
RUN apt update -q \
    && apt upgrade -y -q \
    && apt install -y --no-install-recommends \
    software-properties-common \
    python3-pip \
    xauth \
    sudo \
    gazebo libgazebo-dev \
    ros-humble-gazebo-ros-pkgs \
    # ===== Joystick =====
    ros-humble-joy \
    ros-humble-teleop-twist-joy \
    joystick \
    evtest \
    udev \
    # ===== Common tools =====
    build-essential \
    git \
    vim \
    cmake \
    gdb \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

# ----------------------------
# Create user
# ----------------------------
RUN groupadd -g $GID $USERNAME \
    && useradd -lm -u $UID -g $USERNAME -s /bin/bash $USERNAME \
    && echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER $USERNAME

# ----------------------------
# Workspace
# ----------------------------
RUN mkdir -p /home/$USERNAME/ros2_ws/src
WORKDIR /home/$USERNAME/ros2_ws

# ----------------------------
# Bashrc
# ----------------------------
RUN echo "source /opt/ros/$ROS_DISTRO/setup.bash" >> /home/$USERNAME/.bashrc \
    && echo "source /home/$USERNAME/ros2_ws/install/setup.bash" >> /home/$USERNAME/.bashrc

# ----------------------------
# Entrypoint
# ----------------------------
COPY ./ros_entrypoint.sh /
ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]
