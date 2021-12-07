import numpy as np 
from potentialfield3 import potentialField
from obstacles import Obstacles
from ownship import OwnShip
import matplotlib.pyplot as plt
from plotting import Plotting
from matplotlib.collections import LineCollection
import math


#Simulator variables
t_sim = 1000
t = 0

#Init variables

#Size of the grid
x_sim = 400
y_sim = 400

x = np.arange(-0,400,1)
y = np.arange(-0,400,1)

X, Y = np.meshgrid(x,y)

#Ownship
ownship_traj = np.linspace((0,0), (100,100), t_sim)
ship = OwnShip(ownship_traj[0], ownship_traj)

ship_path_x = [0]
ship_path_y = [0]


#Obstacles
#Define pos of stationairy obstacles
stationary_obstacles = [[]]

#Define init state of dynamic variables [2*pos, 2*velocity, 2*heading]
dynamic_obstacles = np.array([[100, 0, -1,1, 270]])
obs = Obstacles(stationary_obstacles, dynamic_obstacles, t_sim)

field = potentialField(x_sim, y_sim)
obstacles, traj = obs.getObstacles(ownship_traj)


#targets = obs.create_targets(obstacles,ownship_traj[0])

while t<t_sim:
  print(t)
  #get attack angle 
  ship_pos = ship.getPos()

  if ship_pos[0] > 50 or ship_pos[1]>50:
    targets = []
  else: 
    targets = obs.create_targets(obstacles,ship.getPos(), t)



  goal = ship.getGoal(t)


  delx, dely, X, Y = field.makeField(goal, targets, ship.getPos())

  ship.updatePos(delx, dely)

  ship_pos = ship.getPos()
  ship_path_x.append(ship_pos[0])
  ship_path_y.append(ship_pos[1])

  #if ship_pos[0] > 90 or ship_pos[1]>90: 
  #  break


  t = t+1

  #plt.plot(ship_path_x, ship_path_y)
  #plt.plot(targets[:,0], targets[:,1])
  #plt.show()



#plt.plot(targets[:,0], targets[:,1])
#plt.show()

t = np.linspace(0,1,len(ship_path_x))
points1 = np.array([ship_path_x, ship_path_y]).transpose().reshape(-1,1,2)
points2 = np.array([traj[:,:,0], traj[:,:,1]]).transpose().reshape(-1,1,2)

segs1 = np.concatenate([points1[:-1],points1[1:]], axis=1)
segs2 = np.concatenate([points2[:-1],points2[1:]], axis=1)

# make the collection of segments
lc1 = LineCollection(segs1, cmap=plt.get_cmap('jet'))
lc2 = LineCollection(segs2, cmap=plt.get_cmap('jet'))

lc1.set_array(t) # color the segments by our parameter
lc2.set_array(t) 

# plot the collection
plt.gca().add_collection(lc1) # add the collection to the plot
plt.gca().add_collection(lc2) # add the collection to the plot

plt.xlim(0, 100) # line collections don't auto-scale the plot
plt.ylim(0,100)

plt.show()

