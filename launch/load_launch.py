from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    drix_number_arg = DeclareLaunchArgument('drixNumber')
    namespace_arg = DeclareLaunchArgument(
        'namespace',
        default_value=['project11/drix_', LaunchConfiguration('drixNumber')]
    )
    model_arg = DeclareLaunchArgument(
        'model',
        default_value=PathJoinSubstitution(
            [FindPackageShare('drix_description'), 'urdf', 'drix_mesh.xacro']
        )
    )

    robot_description = Command([
        FindExecutable(name='xacro'), ' ',
        LaunchConfiguration('model'),
        ' drixNumber:=', LaunchConfiguration('drixNumber'),
        ' namespace:=', LaunchConfiguration('namespace'),
    ])

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        namespace=LaunchConfiguration('namespace'),
        parameters=[{'robot_description': ParameterValue(robot_description, value_type=str)}],
    )

    return LaunchDescription([
        drix_number_arg,
        namespace_arg,
        model_arg,
        robot_state_publisher_node,
    ])
