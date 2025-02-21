# Cart-Pole Optimal Control Assignment

[Watch the demo video](https://drive.google.com/file/d/1UEo88tqG-vV_pkRSoBF_-FWAlsZOLoIb/view?usp=sharing)
![image](https://github.com/user-attachments/assets/c8591475-3676-4cdf-8b4a-6539e5a2325f)

## Overview
This assignment challenges students to tune and analyze an LQR controller for a cart-pole system subject to earthquake disturbances. The goal is to maintain the pole's stability while keeping the cart within its physical constraints under external perturbations. The earthquake force generator in this assignment introduces students to simulating and controlling systems under seismic disturbances, which connects to the Virtual Shake Robot covered later in the course. The skills developed here in handling dynamic disturbances and maintaining system stability will be useful for optimal control of space robots, such as Lunar landers or orbital debris removal robots.

## System Description
The assignment is based on the problem formalism here: https://underactuated.mit.edu/acrobot.html#cart_pole
### Physical Setup
- Inverted pendulum mounted on a cart
- Cart traversal range: ±2.5m (total range: 5m)
- Pole length: 1m
- Cart mass: 1.0 kg
- Pole mass: 1.0 kg

### Disturbance Generator
The system includes an earthquake force generator that introduces external disturbances:
- Generates continuous, earthquake-like forces using superposition of sine waves
- Base amplitude: 15.0N (default setting)
- Frequency range: 0.5-4.0 Hz (default setting)
- Random variations in amplitude and phase
- Additional Gaussian noise

## Submission

### Understanding LQR
LQR controller stands for a Linear Quadratic Controller. As the name suggests it controlls a linear system by using a cost fucntion which is quadratic in nature. The most integral part of a LQR controller are the cost fucntions. As the name suggests cost functions are basically a penalty to the deviations from the setpoint (suppose origin). Usually in the real world to control an inherently unstable system or a stable system and make is more stable energy is required hence LQR controller puts up a constraint on the controller input too which means LQR penalizes large control inputs. 

The cost function is given by 
J = ∫(x'Q x + u'R u)dt limits of the integral can be set accordingly. Q penalizes deviations in state variables and R penalizes the control input. From this we solve something called a Ricciati Equation and then we find the K which is our controller. 

LQR controller is given by the equation

u = -Kx

### System and Other Important matrices
Our state space representation is as follows :
x_dot = Ax + Bu.

Now we know we are using a LQR controller hence u = -Kx which gives us:

x_dot = (A-B*K)x

First we verify if the system is controllable by finding the rank of the observability matrix A and B. If its rank is equal to the number of state variables we can make our system stable which we can do in our case.

Now what I do is I take a close look at the matrix (A - B*K). The eigen values of the matrix tell me stability of the system if they are in the left half plane my system is stable this is a crude way but is the one I followed to compute the gains. 
To compute the eigenvalues I used matlab's eigen() function.

### Computing state penalties

Why change the default parameters ?
Default parameters were Q = diag[1 1 10 10] and R = 0.1
the eigen values are

-11.9192 + 0.0000i
-2.3126 + 1.5118i
-2.3126 - 1.5118i
-1.0229 + 0.0000i

system seems stable but it goes down after some seconds of operation. Hence what I try here if I could place an eigen value towards far left which increases the stability of the system while not letting any of the other eigen value to become positive.

I start with penalizing x 

![image](https://github.com/user-attachments/assets/4e15aed3-9cab-4810-b0a7-9c6920e6b8f3)

From this I observed that penalizing x does not do much to the eigen values i.e. making the system more stable. Therefore I take an intermediate value of 50 as x's penalty.

Then I move on with penalizing x_dot

![image](https://github.com/user-attachments/assets/018ca5ab-7f34-436f-9589-5a4e178a2557)

I see that increasing the penalty for x_dot also stats bringing an eigen value closer to the origin which means the system kind of it moving towards unstability. Hence I do not crank up the penalty but settle for x_dot's penalty to be 60.

Penalizing theta

![image](https://github.com/user-attachments/assets/885f6607-f2bf-4a99-a103-78460d9a6abc)

Penalizing theta does not do much. It can be noticed when I penalize it with 500 units but still the eigen values do not change much. Therefor I settle for the default value for theta

Penalizing theta_dot

![image](https://github.com/user-attachments/assets/60df8359-9d25-46bc-8fdd-13d6001c4007)

Now when I start penalizing theta_dot my eigen value start moving towards far left. Not one pole starts deceasing. Noticing how moving from 200 - 500 eigen value almost doubles but the observable effect on the cart pole was minimal hence I settle for 100. Another reason for settling for this value is to keep this one root on the left half plane and also because after this the cart pole was observably stable.

Penalizing controller Input - 

![image](https://github.com/user-attachments/assets/28430bb2-51e4-4536-a210-e7a2569295b4)


Eigen value moves towards far left as R decreases so why did I settle for R's default value. When I set R to be 0.01 the cart pole crashed and went down therefore I did not change its value.

### Output

Q matrix is diag (50,60,10,100) and R is 0.1

https://github.com/user-attachments/assets/e97a8984-76a9-4840-aae6-f96258e96a6f

Below shows how the force remains low throughout only sometimes crosses 50 N.
![image](https://github.com/user-attachments/assets/77b439be-d730-4541-b6e8-d57be216be9b)

Below are the plots of  X, theta, X_dot and theta_dot which show that there is inital deviation after which the system becomes pretty stable
![image](https://github.com/user-attachments/assets/17836392-f3f5-4068-9b19-b8df6ce21fca)

### Challenges 
While understanding LQR, one of the challenges was to understand Ricciati equation which I am still trying to figure out and with it the math behind finding K. Understanding the total cart pole system also did pose a challenge but its modular structure made me understand system and how data and messages flow between different nodes which I could use in my future projects.
## License
This work is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).
[![Creative Commons License](https://i.creativecommons.org/l/by/4.0/88x31.png)](http://creativecommons.org/licenses/by/4.0/) 
