import numpy as np
import math 

class Obstacles():


    def __init__(self, stationary_pos, dynamic_state, simulation_time):
        self.stationary_pos = stationary_pos
        self.dynamic_state = dynamic_state #en nd array med [2*position, 2*velocity, heading]
        self.sim_time = simulation_time

    
    def getStationaryObstacles(self): 
        return self.stationary_pos
    
    def getDynamicObstaclesPos(self): 
        return self.dynamic_state[:,:2] #Få kun ut posisjon ikke heading eller velocity så bare ta de to første elementene i en np array?

    def makeObstacleTrajectory(self): 
        #Kinda sucky think, but it should work! Make sure that the indexes are correct!!!

        traj = np.empty((self.dynamic_state.shape[0],self.sim_time, 3))
        for i in range(self.dynamic_state.shape[0]): 
            for t in range(self.sim_time): 
                if t == 0:
                    traj[i,t,0] = self.dynamic_state[i,0]
                    traj[i,t,1] = self.dynamic_state[i,1]
                    traj[i,t,2] = t
                else:
                    traj[i,t,0] = traj[i,t-1,0] + self.dynamic_state[i,2]
                    traj[i,t,1] = traj[i,t-1,1] + self.dynamic_state[i,3]
                    traj[i,t,2] = t
        return traj

    def getObstacles(self, ownship_traj):
        #This function breaks or makes this whole project!!
        #Finding the obstacles that are on impact route

        radi = 5 #The radius of the cirle that i think the obstacle should hit on
        traj = self.makeObstacleTrajectory()
        crash_obstacle = []


        for i in range(traj.shape[0]): #Make sure the shape index is correct aka nr of obstacles
            for t in range(self.sim_time): 
                dist = math.sqrt((ownship_traj[t,0]-traj[i,t,0])**2+(ownship_traj[t,1]-traj[i,t,1])**2)
                if dist < radi: 
                    obstacle_class = self.classifyCollision(traj[:,:,i], ownship_traj)
                    crash_obstacle.append([traj[i,t,0], traj[i,t,1], obstacle_class])
                    
        return crash_obstacle, traj

    def classifyCollision(self, obstacle_traj, ownship_traj): 
        #Try to just make it for rule 15 Give-way
        return("Give-way")



