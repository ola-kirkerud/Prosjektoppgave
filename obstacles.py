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

        traj = np.empty((3,self.sim_time, self.dynamic_state.shape[1]))
        for i in range(self.dynamic_state.shape[1]): #Husker ikke om det er riktig å velge 1 index, tror det er det
            for t in range(self.sim_time): 
                if i == 0:
                    traj[0,t,i] = self.dynamic_state[0,i]
                    traj[1,t,i] = self.dynamic_state[1,i]
                    traj[2,t,i] = t
                else:
                    traj[0,t,i] = traj[0,t-1,i] + self.dynamic_state[2,i]*t
                    traj[1,t,i] = traj[1,t-1,i] + self.dynamic_state[3,i]*t
            
        return traj

    def getObstacles(self, ownship_traj):
        #This function breaks or makes this whole project!!
        #Finding the obstacles that are on impact route

        radi = 10 #The radius of the cirle that i think the obstacle should hit on
        traj = self.makeObstacleTrajectory()
        crach_obstacle = []

        for i in range(traj.shape[2]): #Make sure the shape index is correct aka nr of obstacles
            for t in range(self.sim_time): 
                dist = math.sqrt((ownship_traj[0,t,i]-traj[0,t,i]^2)+(ownship_traj[1,t,i]-traj[1,t,i]^2))
                if dist < radi: 
                    obstacle_class = self.classifyCollision(traj[_,_,i], ownship_traj)
                    crach_obstacle.append([traj[0,t,i], traj[1,t,i], obstacle_class])
                    
        return crach_obstacle

    def classifyCollision(obstacle_traj, ownship_traj): 
        #Try to just make it for rule 15 Give-way
        return("Give-way")



