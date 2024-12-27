from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
# from launch_ros.parameter_descriptions import ParameterValue
# import os
# from ament_index_python.packages import get_package_share_directory
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Define the path to your URDF file
    
    urdf_path = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [FindPackageShare("dynamixel_manipulator"), "urdf", "standalone.urdf.xacro"]
            ),
        ]
    )

    robot_description = {"robot_description": urdf_path}

    robot_controllers = PathJoinSubstitution(
        [
            FindPackageShare("dynamixel_manipulator"),
            "config",
            "controller_config.yaml",
        ]
    )


    rviz_config_file = PathJoinSubstitution(
        [
            FindPackageShare("dynamixel_manipulator"), "rviz", "urdf_config.rviz"
        ]
    )

    # Node for the controller manager
    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[robot_description, robot_controllers],
        output="both",
    )

    robot_state_pub_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="both",
        parameters=[robot_description],
    )

    # Spawner for joint state broadcaster
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "--controller-manager",
            "/controller_manager",
        ]
    )

    # Spawner for arm controller
    arm_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "arm_controller",
            "--controller-manager",
            "/controller_manager",
        ]
    )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="log",
        arguments=["-d", rviz_config_file],
    )

    return LaunchDescription([
        rviz_node,
        robot_state_pub_node,
        controller_manager,
        joint_state_broadcaster_spawner,
        arm_controller_spawner
    ])

