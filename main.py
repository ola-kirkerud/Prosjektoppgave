import numpy as np 
from potentialfield import potentialField
from obstacles import Obstacles
from ownship import OwnShip
import matplotlib.pyplot as plt
from plotting import Plotting


#Simulator variables
t_sim = 100
t = 0

#Init variables

#Size of the grid
x_sim = 200
y_sim = 200

x = np.arange(-0,200,1)
y = np.arange(-0,200,1)

X, Y = np.meshgrid(x,y)

#Ownship
ownship_traj = np.linspace((0,0), (100,100), t_sim)
ship = OwnShip(ownship_traj[0], ownship_traj)

print(ownship_traj[0])

ship_path_x = [0]
ship_path_y = [0]


#Obstacles
#Define pos of stationairy obstacles
stationary_obstacles = [[]]

#Define init state of dynamic variables [2*pos, 2*velocity, 2*heading]
dynamic_obstacles = np.array([[0, 50, 1,0, 270]])
obs = Obstacles(stationary_obstacles, dynamic_obstacles, t_sim)

field = potentialField(x_sim, y_sim)

while t<t_sim:

  obstacles, traj = obs.getObstacles(ownship_traj)
  #obstacles = [[50,100]]
  print("obs")
  print(obstacles)
  goal = ship.getGoal(t)
  print("goal")
  print(goal)
  print("pos")


  delx, dely, X, Y = field.makeField(goal, obstacles)
  #fig, ax = plt.subplots(figsize=(10,10))
  #ax.quiver(X, Y, delx, dely)
  #plt.show()
  ship.updatePos(delx, dely)

  ship_pos = ship.getPos()
  ship_path_x.append(ship_pos[0])
  ship_path_y.append(ship_pos[1])


  print(ship_pos)

  t = t+1
plt.plot(ship_path_x, ship_path_y, linestyle = 'dotted')
plt.show()
Plotting.lineplot(ship_path_x, ship_path_y)


