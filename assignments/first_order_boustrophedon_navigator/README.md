# First-Order Boustrophedon Navigator
![image](https://github.com/user-attachments/assets/940fc6bc-fcee-4d11-8bc8-d53a650aaf80)

In this assignment, you will understand the provided code in ROS2 with Turtlesim, and refactor and/or tune the navigator to implement a precise lawnmower survey (a boustrophedon pattern). The current code will do a pattern shown above, which is not a uniform lawnmower survey. 
Explore literature on how lawnmower surveys typically look, and modify the code to meet the requirements for a uniform survey. 

## Background
Boustrophedon patterns (from Greek: "ox-turning", like an ox drawing a plow) are fundamental coverage survey trajectories useful in space exploration and Earth observation. These patterns are useful for:

- **Space Exploration**: Rovers could use boustrophedon patterns to systematically survey areas of interest, ensuring complete coverage when searching for geological samples or mapping terrain. However, due to energy constraints, informative paths are usually optimized, and this results in paths that are sparser than complete coverage sampling, and may still produce high-accuracy reconstructions. 
  
- **Earth Observation**: Aerial vehicles employ these patterns for:
  - Agricultural monitoring and precision farming
  - Search and rescue operations
  - Environmental mapping and monitoring
  - Geological or archaeological surveys
  
- **Ocean Exploration**: Autonomous underwater vehicles (AUVs) use boustrophedon patterns to:
  - Map the ocean floor
  - Search for shipwrecks or aircraft debris
  - Monitor marine ecosystems
  
The efficiency and accuracy of these surveys depend heavily on the robot's ability to follow the prescribed path with minimal deviation (cross-track error). This assignment simulates these real-world challenges in a 2D environment using a first-order dynamical system (the turtlesim robot).

## Objective
Tune a PD controller to make a first-order system execute the most precise boustrophedon pattern possible. The goal is to minimize the cross-track error while maintaining smooth motion.

## Learning Outcomes
- Understanding PD control parameters and their effects on first-order systems
- Practical experience with controller tuning
- Analysis of trajectory tracking performance
- ROS2 visualization and debugging

## Prerequisites

### System Requirements
Choose one of the following combinations:
- Ubuntu 22.04 + ROS2 Humble
- Ubuntu 23.04 + ROS2 Iron
- Ubuntu 23.10 + ROS2 Iron
- Ubuntu 24.04 + ROS2 Jazzy

### Required Packages
```bash
sudo apt install ros-$ROS_DISTRO-turtlesim
sudo apt install ros-$ROS_DISTRO-rqt*
```

### Python Dependencies
```bash
pip3 install numpy matplotlib
```

## The Challenge

### 1. Controller Tuning (60 points)
Use rqt_reconfigure to tune the following PD controller parameters in real-time:
```python
# Controller parameters to tune
self.Kp_linear = 1.0   # Proportional gain for linear velocity
self.Kd_linear = 0.1   # Derivative gain for linear velocity
self.Kp_angular = 1.0  # Proportional gain for angular velocity
self.Kd_angular = 0.1  # Derivative gain for angular velocity
```

Performance Metrics:
- Average cross-track error (25 points)
- Maximum cross-track error (15 points)
- Smoothness of motion (10 points)
- Cornering performance (10 points)

### 2. Pattern Parameters (20 points)
Optimize the boustrophedon pattern parameters:
```python
# Pattern parameters to tune
self.spacing = 1.0     # Spacing between lines
```
- Coverage efficiency (10 points)
- Pattern completeness (10 points)

### 3. Analysis and Documentation (20 points)
Provide a detailed analysis of your tuning process:
- Methodology used for tuning
- Performance plots and metrics
- Challenges encountered and solutions
- Comparison of different parameter sets

## Getting Started

### Repository Setup
1. Fork the course repository:
   - Visit: https://github.com/DREAMS-lab/RAS-SES-598-Space-Robotics-and-AI
   - Click "Fork" in the top-right corner
   - Select your GitHub account as the destination

2. Clone your fork (outside of ros2_ws):
```bash
cd ~/
git clone https://github.com/YOUR_USERNAME/RAS-SES-598-Space-Robotics-and-AI.git
```

3. Create a symlink to the assignment in your ROS2 workspace:
```bash
cd ~/ros2_ws/src
ln -s ~/RAS-SES-598-Space-Robotics-and-AI/assignments/first_order_boustrophedon_navigator .
```

### Building and Running
1. Build the package:
```bash
cd ~/ros2_ws
colcon build --packages-select first_order_boustrophedon_navigator
source install/setup.bash
```

2. Launch the demo:
```bash
ros2 launch first_order_boustrophedon_navigator boustrophedon.launch.py
```

3. Monitor performance:
```bash
# View cross-track error as a number
ros2 topic echo /cross_track_error

# Or view detailed statistics in the launch terminal
```

4. Visualize trajectory and performance:
```bash
ros2 run rqt_plot rqt_plot
```
Add these topics:
- /turtle1/pose/x
- /turtle1/pose/y
- /turtle1/cmd_vel/linear/x
- /turtle1/cmd_vel/angular/z
- /cross_track_error

## Evaluation Criteria

1. Controller Performance (60%)
   - Average cross-track error < 0.2 units (25%)
   - Maximum cross-track error < 0.5 units (15%)
   - Smooth velocity profiles (10%)
   - Clean cornering behavior (10%)

2. Pattern Quality (20%)
   - Even spacing between lines
   - Complete coverage of target area
   - Efficient use of space

3. Documentation (20%)
   - Clear explanation of tuning process
   - Well-presented performance metrics
   - Thoughtful analysis of results

## Submission

1. Tuning Process
   -Tuning process started off by checking the trivial cases i.e. setting Kp_linear to 1 and Kp_angular to 1 and checking how the turtlesim behaves. With the proportional values set to 1 and Dervative part set to 0.1 we get the following outcome -   

![Screenshot from 2025-01-27 20-25-16](https://github.com/user-attachments/assets/2da9032f-19cf-44db-a39d-fdf247a054ee)
We know that v=w.r( linear_velocity = angular_velocity*radius). Using this we infer that radius is v/w( linear_velocity/angular_velocity). So we want the radius to be larger ( infinite ideally to emulate a straight line).
Due to this reason I increase the Kp_angular. Increase it and not decrease it because I want angular velocity to tend to zero as quickly as possible.

Using this hypothesis I increase Kp_angular. Next iteration is Kp_linear = 1 and Kp_angular = 5
![Screenshot from 2025-01-27 20-57-57](https://github.com/user-attachments/assets/0771df7e-0af7-4944-a753-2c908f092158)
We could see that there still is a helix like structure but with decreased radius. Assuming there still is some problem with kp_angular. I further take a step in coarse tuning and change it to 7.
![Screenshot from 2025-01-27 21-04-52](https://github.com/user-attachments/assets/105625ce-9c4d-45b5-9e7c-f617dea35d0a)

Setting kp_angular to 7 we can further see that now it is not a helix anymore but we get something similar to our pattern. But again we notice that the linear velocity is problem so I start with tuning Kp_linear to 2

![Screenshot from 2025-01-27 21-10-25](https://github.com/user-attachments/assets/b12f7b6b-5630-4f3c-b435-eb622e566bd9)

This setting gives final cross tracker error to be 0.144 but the maximum value of the the same is 0.3. So, I further go forward with coarse tuning and change Kp_linear to 3 to check if error drops down and I get a smoother curve.

![Screenshot from 2025-01-27 21-21-00](https://github.com/user-attachments/assets/37c98ae0-0370-477b-afb1-b4d6f8c6b907)

This gives the same value so I try with more aggressive tuning I move Kp_linear to 5 and check the results.

![Screenshot from 2025-01-27 21-24-56](https://github.com/user-attachments/assets/e3f88514-b0d9-4624-b392-73a0b68ad324)

the performance around the corners is bad therefore I tune Kp_angular to 8.

![Screenshot from 2025-01-27 21-30-15](https://github.com/user-attachments/assets/1ee91c2e-0ffa-440e-af78-4fddabe6acf9)

This reduces average cross track error to 0.11 and max cross track error to 0.245. Continuing the tuning process I changed Kp_angular to 9 which improved the results further average cross track error to 0.092 and maximum cross track error changes to 0.208.

![Screenshot from 2025-01-27 21-44-16](https://github.com/user-attachments/assets/ca6b5516-8860-479d-b505-a9b3860c71ee)

Fixing the values of Kp_linear = 5 and Kp_angular = 9.5. As the tuning requirments are met I do not change the values of derivative controller. Below are the plots of the linear and angular velocities and the pose of turtle. 

![Screenshot from 2025-01-27 22-23-33](https://github.com/user-attachments/assets/e4d613db-2ee0-4b2f-819d-8235f6f31d42)

2. Final Values
   -The final values are as follows Kp_linear = 5, Kd_angular = 0.1, Kp_angular = 9.5, Kd_angular = 0.1. spacing = 0.5( to accomodate larger area) and max speed = 2.
   ![Screenshot from 2025-01-27 22-46-40](https://github.com/user-attachments/assets/950a8f1c-9e9c-4cfb-9db8-eaeb5e5f8526)

