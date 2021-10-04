#Import libraries
import numpy as np
import matplotlib.pyplot as plt
import random

#Set all the stationary obstacles
obs1 = [5,5]

#Set all the dynamic obstacles with start position and velocity


#Set the position of the OS 
os = [1,1]

#Set the end position
end = [100,100]


#Set a trajectory from A to B that does not collide in the stationairy obstacles
coefficients = np.polyfit([os[0],end[0]], [os[1],end[1]], 1)

polynomial = np.poly1d(coefficients)
x_axis = np.linspace(0,100,200)
y_axis = polynomial(x_axis)

t_sim = 200
t = 0

x = np.arange(-0,100,1)
y = np.arange(-0,100,1)
s = 7
r=2
seek_points = np.array([[0,0]]) 
X, Y = np.meshgrid(x,y)
def add_goal (X, Y,s, r, loc):

  delx = np.zeros_like(X)
  dely = np.zeros_like(Y)
  for i in range(len(X)):
    for j in range(len(Y)):
      
      d= np.sqrt((loc[0]-X[i][j])**2 + (loc[1]-Y[i][j])**2)
      #print(f"{i} and {j}")
      theta = np.arctan2(loc[1]-Y[i][j], loc[0] - X[i][j])
      if d< r:
        delx[i][j] = 0
        dely[i][j] =0
      elif d>r+s:
        delx[i][j] = 50* s *np.cos(theta)
        dely[i][j] = 50 * s *np.sin(theta)
      else:
        delx[i][j] = 50 * (d-r) *np.cos(theta)
        dely[i][j] = 50 * (d-r) *np.sin(theta)
  return delx, dely

s = 7
r = 2
for i in range(x_axis.size):
    goal = [x_axis[i], y_axis[i]]
    delx,dely = add_goal(X, Y, s, r, goal)


print(delx)
fig, ax = plt.subplots(figsize = (10,10))
ax.quiver(X, Y, delx, dely)
ax.add_patch(plt.Circle((100, 100), 2, color='b'))
ax.annotate("Goal", xy=(0, 0), fontsize=20, ha="center")
ax.set_title('Attractive field of the Goal')
plt.show() 

#while t < t_sim: 


#while simulation is going on 

        #For each dynamic obstacle calculate the path with position and time. 

    #Make an attractive potential field to the trajectory points

    #Find where the OS will collide with another ship 

    #Classify the situation with the other ship 

    #Might need to do the 3 above in the for loop

    #Make a repulsive potential field based on the stationary obstacles and the dynamic obstacles 

    #Combine both potential fields

    #Make some simple ship dynamic that translate the forces of the potential field to movement 

#Plot the results
    
