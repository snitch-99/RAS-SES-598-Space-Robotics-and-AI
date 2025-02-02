from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import os

def generate_launch_description():
    pkg_share = FindPackageShare('inverted_pendulum_optimal_control').find('inverted_pendulum_optimal_control')
    urdf_model_path = os.path.join(pkg_share, 'models', 'inverted_pendulum', 'model.urdf')
    
    return LaunchDescription([
        # Robot state publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[{'robot_description': Command(['cat ', urdf_model_path])}]
        ),

        # Gazebo
        ExecuteProcess(
            cmd=['gz', 'sim', '-r', 'empty.sdf'],
            output='screen'
        ),

        # Direct topic bridges
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='bridge',
            output='screen',
            arguments=[
                # Cart force command (ROS -> Gazebo)
                '/model/inverted_pendulum/joint/cart_to_base/cmd_force@std_msgs/msg/Float64]gz.msgs.Double',
                # Joint states (Gazebo -> ROS)
                '/world/empty/model/inverted_pendulum/joint_state@sensor_msgs/msg/JointState[ignition.msgs.Model',
                # Clock (Gazebo -> ROS)
                '/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock'
            ],
        ),

        # Spawn robot
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-topic', 'robot_description',
                '-name', 'inverted_pendulum',
                '-allow_renaming', 'true'
            ],
            output='screen'
        ),

        # Controller
        Node(
            package='inverted_pendulum_optimal_control',
            executable='lqr_controller',
            name='lqr_controller',
            output='screen'
        )
    ]) 