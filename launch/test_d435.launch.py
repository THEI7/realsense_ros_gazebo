from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, Command, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue  # 👈 新增导入
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    pkg_share = FindPackageShare('realsense_ros_gazebo')
    gazebo_ros_pkg_share = FindPackageShare('gazebo_ros')

    # 使用 Command 延迟执行 xacro，并包装为字符串参数
    urdf_file = PathJoinSubstitution([pkg_share, 'urdf', 'test.xacro'])
    robot_description = ParameterValue(Command(['xacro ', urdf_file]), value_type=str)  # 👈 关键修改！

    world_path = PathJoinSubstitution([gazebo_ros_pkg_share, 'worlds', 'empty.world'])

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    )

    declare_world_cmd = DeclareLaunchArgument(
        'world',
        default_value=world_path,
        description='Full path to world model file to load'
    )

    declare_gui_cmd = DeclareLaunchArgument(
        'gui',
        default_value='true',
        description='Set to "false" to run headless.'
    )

    declare_verbose_cmd = DeclareLaunchArgument(
        'verbose',
        default_value='false',
        description='Set to "true" to enable verbose output'
    )

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([gazebo_ros_pkg_share, 'launch', 'gazebo.launch.py'])
        ),
        launch_arguments={
            'world': LaunchConfiguration('world'),
            'gui': LaunchConfiguration('gui'),
            'verbose': LaunchConfiguration('verbose'),
            'use_sim_time': LaunchConfiguration('use_sim_time')
        }.items()
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'robot_description': robot_description  # 已正确包装为字符串
        }]
    )

    spawn_entity_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'test_model',
            '-topic', 'robot_description',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.0'
        ],
        output='screen'
    )

    return LaunchDescription([
        declare_use_sim_time_cmd,
        declare_world_cmd,
        declare_gui_cmd,
        declare_verbose_cmd,
        gazebo_launch,
        robot_state_publisher_node,
        spawn_entity_node
    ])