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
        traj = np.linspace((100, 0,0), (0, 100,self.sim_time),self.sim_time).reshape((1,self.sim_time,3))

        return traj

    def getObstacles(self, ownship_traj):
        #This function breaks or makes this whole project!!
        #Finding the obstacles that are on impact route

        radi = 5 #The radius of the cirle that i think the obstacle should hit on
        traj = self.makeObstacleTrajectory()
        #crash_obstacle = []
        crash_obstacle = np.array([[0,0]])

        for i in range(traj.shape[0]): #Make sure the shape index is correct aka nr of obstacles
            for t in range(self.sim_time): 
                dist = math.sqrt((ownship_traj[t,0]-traj[i,t,0])**2+(ownship_traj[t,1]-traj[i,t,1])**2)
                if dist < radi: 
                    obstacle_class = 'Giwe-way'#self.classifyCollision(traj[:,:,i], ownship_traj)
                    #crash_obstacle.append([traj[i,t,0], traj[i,t,1], obstacle_class])
                    crash_obstacle = np.append(crash_obstacle, [[traj[i,t,0], traj[i,t,1]]], axis=0)

        obstacle = [obstacle_class, crash_obstacle[1:,0].sum()/(crash_obstacle.shape[0]-1),crash_obstacle[1:,1].sum()/(crash_obstacle.shape[0]-1)] 

                    
        return obstacle, traj

    def create_targets(self, obstacle, own_ship_pos): 
        r = math.sqrt((own_ship_pos[0]-obstacle[1])**2 + (own_ship_pos[1]-obstacle[2])**2)

        phi = 2*math.pi/2 #225 degrees should define phi from r
        end = [obstacle[1], obstacle[2]-20]


        x = np.flip(np.linspace(end[0]+math.cos(phi)*40,end[0], 10)).reshape((10,1))
        y = (np.linspace(end[1],end[1]+math.sin(phi)*40, 10)).reshape((10,1))


        return np.hstack((x,y))

    def classifyCollision(self, obstacle_traj, ownship_traj): 
        #Try to just make it for rule 15 Give-way

        return("Give-way")



