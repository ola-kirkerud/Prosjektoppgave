import numpy as np 
from potentialfield import potentialField
from obstacles import Obstacles
from ownship import OwnShip
import matplotlib.pyplot as plt
from plotting import Plotting
from matplotlib.collections import LineCollection


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
print(obstacles, traj)

obstacles = [[48.8,49.6],[47,50],[45.47,50.1],[43.13,50.8],[40.66,51.1]]

while t<t_sim:

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

#fig = plt.plot()
#plt.quiver(X,Y,delx,dely)
#plt.plot(ship_path_x, ship_path_y, linestyle = 'dotted')
#plt.show()
#Plotting.lineplot(ship_path_x, ship_path_y)

t = np.linspace(0,1,len(ship_path_x))
points1 = np.array([ship_path_x, ship_path_y]).transpose().reshape(-1,1,2)
points2 = np.array([traj[:,:,0], traj[:,:,1]]).transpose().reshape(-1,1,2)
print(points1)
print(points2)

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

