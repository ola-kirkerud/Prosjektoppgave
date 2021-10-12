import numpy as np 
from potentialfield import potentialField
from obstacles import Obstacles
from ownship import OwnShip



#Simulator variables
t_sim = 200
t = 0

#Init variables

#Size of the grid
x_sim = 200
y_sim = 200

#Ownship
ownship_traj = np.linspace((1,1), (200,200), 200)
ship = OwnShip(ownship_traj[0], ownship_traj)

#Obstacles
#Define pos of stationairy obstacles
stationary_obstacles = [[]]

#Define init state of dynamic variables [2*pos, 2*velocity, 2*heading]
dynamic_obstacles = [[100, 50, -1,1, 270]]

obs = Obstacles(stationary_obstacles, dynamic_obstacles, t_sim)

field = potentialField(x_sim, y_sim)

while t<t_sim:

  obstacles = obs.getObstacles(ownship_traj)

  delx, dely = field.makeField(goal, obstacles)

  ship.updatePos(delx, dely)


