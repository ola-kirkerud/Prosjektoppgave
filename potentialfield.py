#Import libraries
import numpy as np
import matplotlib.pyplot as plt
import sys
import random
#np.set_printoptions(threshold=sys.maxsize)

class potentialField(): 
  def __init__(self, x_dim, y_dim):
      self.x = np.arange(-0, x_dim, 1)
      self.y = np.arange(-0, y_dim, 1) 

  def make(self, X, Y, delx, dely, obstacle):

    s = 2
    r = 5

    delx = np.zeros_like(X)
    dely = np.zeros_like(Y)

    for i in range(len(self.x)):
      for j in range(len(self.y)):

        d_obstacle = np.sqrt((obstacle[0]-X[i][j])**2 + (obstacle[1]-Y[i][j])**2)
        theta_obstacle = np.arctan2(obstacle[1] - Y[i][j], obstacle[0]  - X[i][j])

        if d_obstacle < r+s:
          delx[i][j] += -150 *(s+r-d_obstacle)* np.cos(theta_obstacle)
          dely[i][j] += -150 * (s+r-d_obstacle)*  np.sin(theta_obstacle) 
    
    return delx, dely
  
  def addGoal(self, X,Y,s,r,loc):
  # X = 2D array of the points on x-axis
  # Y = 2D array of the points on y-axis 
  # r = goal size
  # loc = goal location
    delx = np.zeros_like(X)
    dely = np.zeros_like(Y)

    for x in range(len(self.x)):
      for y in range(len(self.y)):

        d = np.sqrt((loc[0]-x)**2 + (loc[1]-y)**2)
        theta = np.arctan2(loc[1]-y, loc[0]-x)

        if d < r:
          delx[x][y] = 0
          dely[x][y] = 0
        elif d>r+s:
          delx[x][y] = 50* s *np.cos(theta)
          dely[x][y] = 50 * s *np.sin(theta)
        else:
          delx[x][y] = 50 * (d-r) *np.cos(theta)
          dely[x][y] = 50 * (d-r) *np.sin(theta)

    return delx, dely


  def addObstacle(self, X, Y, delx, dely, goal, obstacle): 
    #X = 2d array of the points on the x-axis
    #Y = 2d array of the points on the y-axis 
    #goal = location og the goal


    #s = 4 works okay, very big correction backwards though
    s=4
    r = 5


    for x in range(len(self.x)):
      for y in range(len(self.y)):
        
        d_goal = np.sqrt((goal[0]-x)**2 + ((goal[1]-y))**2)

        d_obstacle = np.sqrt((obstacle[0]-x)**2 + (obstacle[1]-y)**2)
        #print(f"{i} and {j}")
        theta_goal= np.arctan2(goal[1] - x, goal[0]  - y)
        theta_obstacle = np.arctan2(obstacle[1] - y, obstacle[0]  - x)


        #if d_obstacle < r:
        #  delx[i][j] = -1*np.sign(np.cos(theta_obstacle))*5 +0
        #  dely[i][j] = -1*np.sign(np.sin(theta_obstacle))*5 +0
        #if d_obstacle>r+s:
        #  delx[i][j] += 0 -(50 * s *np.cos(theta_goal))
        #  dely[i][j] += 0 - (50 * s *np.sin(theta_goal))
        if d_obstacle<r+s:

          #print(d_obstacle)
          #print(obstacle[0],obstacle[1])
          #print(X[i][j], Y[i][j])
          #print(X[i,j], Y[i,j])

          delx[x][y] += -160 *(s+r-d_obstacle)* np.cos(theta_obstacle)
          dely[x][y] += -160 * (s+r-d_obstacle)*  np.sin(theta_obstacle) 
           

        if d_goal <r+s:
          if delx[x][y] != 0:
            delx[x][y]  += (200 * (d_goal-r) *np.cos(theta_goal))
            dely[x][y]  += (200 * (d_goal-r) *np.sin(theta_goal))
          else:
            
            delx[x][y]  = (50 * (d_goal-r) *np.cos(theta_goal))
            dely[x][y]  = (50 * (d_goal-r) *np.sin(theta_goal))
            
        if d_goal>r+s:
          if delx[x][y] != 0:
            delx[x][y] += 50* s *np.cos(theta_goal)
            dely[x][y] += 50* s *np.sin(theta_goal)
          else:
            
            delx[x][y] = 50* s *np.cos(theta_goal)
            dely[x][y] = 50* s *np.sin(theta_goal) 

        #if d_goal<r:
        #    delx[i][j] = 0
        #    dely[i][j] = 0
    #print("end")
    #print(delx[28,12])
    #print(dely[28,12])
    #print(X[28][12])
    
    return delx, dely, obstacle, r
  


  def makeField(self, goal, obstacles): 
    X, Y = np.meshgrid(self.x, self.y)
    s = 5
    r = 1
    delx, dely = self.addGoal(X,Y,s,r,goal)

    for obstacle in obstacles:
      delx, dely, obstacle, r = self.addObstacle(X, Y, delx, dely, goal, obstacle)
    return delx, dely, X, Y
