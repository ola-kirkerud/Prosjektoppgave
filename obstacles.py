import numpy as np
import math 
import matplotlib.pyplot as plt


class Obstacles():


    def __init__(self, stationary_pos, dynamic_state, simulation_time):
        self.stationary_pos = stationary_pos
        self.dynamic_state = dynamic_state #en nd array med [2*position, 2*velocity, heading]
        self.sim_time = simulation_time
        self.traj = [[]]

    

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

        print(traj)

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
        self.traj = traj
                    
        return obstacle, traj

    def create_targets(self, obstacle, own_ship_pos, t): 
        d_ts_cpa = math.sqrt((obstacle[1]-self.traj[0,t,0])**2 + (obstacle[2]-self.traj[0,t,1])**2)
        d_ts_os = math.sqrt((own_ship_pos[0]-self.traj[0,t,0])**2 + (own_ship_pos[1]-self.traj[0,t,1])**2)
        d_os_cpa = math.sqrt((obstacle[1]-own_ship_pos[0])**2 + (obstacle[2]-own_ship_pos[1])**2)

        #Attack angle between OS and TS
        #A bug that fucks this up...
        attack = np.arccos((d_ts_cpa**2+d_os_cpa**2-d_ts_os**2)/2*d_ts_cpa*d_os_cpa)

        #attack = 1.5707963275688286
        attack = 1.3
        #Angle theta is the heading of TS
        if t>self.sim_time-11:
            theta = np.arctan2(self.traj[0,self.sim_time-10,0]-self.traj[0,-1,0],self.traj[0,self.sim_time-10,1]-self.traj[0,-1,1])
        else: 
            theta = np.arctan2(self.traj[0,t,0]-self.traj[0,t+10,0],self.traj[0,t,1]-self.traj[0,t+10,1])
        if theta<0:
            theta = theta+2*math.pi
        
        k = 10

        #N is the start of the line 
        Nx_start = self.traj[0,t,0] + k*math.cos(theta+math.pi/2)
        Ny_start = self.traj[0,t,1] + k*math.sin(theta+math.pi/2)

        #Phi target is the angle of the line
        if attack > 3*math.pi/4:
            phi_target = theta
        elif attack<=3*math.pi/4:
            phi_target = theta - (12*attack/23 + 89*math.pi/207)

        Nx_end = Nx_start + 50*math.sin(phi_target-math.pi/2)
        Ny_end = Ny_start + 50*math.cos(phi_target-math.pi/2)
      

        x = np.linspace(Nx_start, Nx_end, 60).reshape((60,1))
        y = np.linspace(Ny_start, Ny_end, 60).reshape((60,1))

        #plt.plot(x,y)
        #plt.plot(self.traj[0,t,0],self.traj[0,t,1])
        #plt.show()
        #print(np.hstack((x,y)))
        return np.hstack((x,y))

    def classifyCollision(self, obstacle_traj, ownship_traj): 
        #Try to just make it for rule 15 Give-way

        return("Give-way")



