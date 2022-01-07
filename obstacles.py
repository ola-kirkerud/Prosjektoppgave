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
        #traj = np.linspace((50, 0,0), (50, 100,self.sim_time),self.sim_time).reshape((1,self.sim_time,3)) #90 degrees

        #traj = np.linspace((55, 0,0), (50, 100,self.sim_time),self.sim_time).reshape((1,self.sim_time,3))

        traj = np.linspace((45, 0,0), (50, 100,self.sim_time),self.sim_time).reshape((1,self.sim_time,3))


        return traj

    def getObstacles(self, ownship_traj):
        #This function breaks or makes this whole project!!
        #Finding the obstacles that are on impact route

        radi = 3 #The radius of the cirle that i think the obstacle should hit on
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
        if crash_obstacle.shape[0] == 1:
            obstacle = []
        else:
            obstacle = [obstacle_class, crash_obstacle[1:,0].sum()/(crash_obstacle.shape[0]-1),crash_obstacle[1:,1].sum()/(crash_obstacle.shape[0]-1)] 

        self.traj = traj
        
   
        return obstacle, traj

    def create_targets(self, obstacle, own_ship_pos, t, os_heading): 
        d_ts_cpa = math.sqrt((obstacle[1]-self.traj[0,t,0])**2 + (obstacle[2]-self.traj[0,t,1])**2)
        d_ts_os = math.sqrt((own_ship_pos[0]-self.traj[0,t,0])**2 + (own_ship_pos[1]-self.traj[0,t,1])**2)
        d_os_cpa = math.sqrt((obstacle[1]-own_ship_pos[0])**2 + (obstacle[2]-own_ship_pos[1])**2)

        #Attack angle between OS and TS
        #A bug that fucks this up...
        attack = np.arccos((d_ts_cpa**2+d_os_cpa**2-d_ts_os**2)/2*d_ts_cpa*d_os_cpa)

        #attack = 1.5707963275688286
        attack = 1.2
        #Angle theta is the heading of TS
        if t>self.sim_time-11:
            theta = np.arctan2(self.traj[0,self.sim_time-10,0]-self.traj[0,-1,0],self.traj[0,self.sim_time-10,1]-self.traj[0,-1,1])
        else: 
            theta = np.arctan2(self.traj[0,t,0]-self.traj[0,t+10,0],self.traj[0,t,1]-self.traj[0,t+10,1])
        if theta<0:
            theta = theta+2*math.pi
        
        k = 5

        attack = theta - os_heading
        if attack < 0:
            attack = attack + 2*math.pi

        #N is the start of the line 
        Nx_start = self.traj[0,t,0] + k*math.cos(theta+math.pi/2)
        Ny_start = self.traj[0,t,1] + k*math.sin(theta+math.pi/2)

        #Phi target is the angle of the line
        if attack > 3*math.pi/4:
            phi_target = theta
        elif attack<=3*math.pi/4:
            phi_target = theta - (10*attack/23 + 89*math.pi/207)

        Nx_end = Nx_start + 50*math.sin(phi_target-math.pi/2)
        Ny_end = Ny_start + 50*math.cos(phi_target-math.pi/2)
      

        x = np.linspace(Nx_start, Nx_end, 60).reshape((60,1))
        y = np.linspace(Ny_start, Ny_end, 60).reshape((60,1))

        #plt.plot(x,y)
        #plt.plot(self.traj[0,t,0],self.traj[0,t,1])
        #plt.show()
        #print(np.hstack((x,y)))
        return np.hstack((x,y))

    def create_static_linear_target(self, obstacle, os_pos, os_heading):
        r = math.sqrt((obstacle[1]-os_pos[0])**2 + (obstacle[2]-os_pos[1])**2)

        if r > 40: 
            d = 40
        else:
            d = r/2
        
        theta = 3*math.pi/5

        e_x = os_pos[0] + d*math.cos(os_heading)
        e_y = os_pos[1] + d*math.sin(os_heading)

        k = 12

        e_endx = e_x + k*math.cos(-theta + os_heading - math.pi)
        e_endy = e_y + k*math.sin(-theta + os_heading - math.pi)

        e_startx = e_x - k*math.cos(-theta + os_heading - math.pi)
        e_starty = e_y - k*math.sin(-theta + os_heading - math.pi)

        x = np.linspace(e_startx, e_endx, 60).reshape((60,1))
        y = np.linspace(e_starty, e_endy, 60).reshape((60,1))
        #plt.plot(x,y)
        #plt.plot(self.traj[0,t,0],self.traj[0,t,1])
        #plt.show()
        #print(np.hstack((x,y)))
        return np.hstack((x,y))

    def create_dynamic_linear_line(self, t):
        r = 25
        ts_heading = np.arctan2(self.traj[0,10,1]-self.traj[0,0,1], self.traj[0,10,0] - self.traj[0,0,0])

        e_x = self.traj[0,t,0] + r*math.cos(ts_heading)
        e_y = self.traj[0,t,1] + r*math.sin(ts_heading)

        #print(e_x, e_y)

        theta = 1*math.pi/4

        k= 12

        e_endx = e_x + k*math.cos(ts_heading - theta)
        e_endy = e_y + k*math.sin(ts_heading - theta)

        e_startx = e_x - k*math.cos(ts_heading - theta)
        e_starty = e_y - k*math.sin(ts_heading - theta)

        x = np.linspace(e_startx, e_endx, 200).reshape((200,1))
        y = np.linspace(e_starty, e_endy, 200).reshape((200,1))
        #plt.plot(x,y)
        #plt.plot(self.traj[0,:,0],self.traj[0,:,1])
        #plt.show()
        #print(np.hstack((x,y)))
        return np.hstack((x,y))


    def create_dynamic_multiple_linear_line(self, t):
        r = 20
        ts_heading = np.arctan2(self.traj[0,10,1]-self.traj[0,0,1], self.traj[0,10,0] - self.traj[0,0,0])

        e_x = self.traj[0,t,0] + r*math.cos(ts_heading)
        e_y = self.traj[0,t,1] + r*math.sin(ts_heading)

        #print(e_x, e_y)
        theta = 1*math.pi/4
        r = 10
        k= 30

        e_endx = e_x + k*math.cos(ts_heading - theta)
        e_endy = e_y + k*math.sin(ts_heading - theta)

        e_startx = e_x - k*math.cos(ts_heading - theta)
        e_starty = e_y - k*math.sin(ts_heading - theta)

        e_parx = e_startx - r*math.cos(ts_heading - math.pi)
        e_pary = e_starty - r*math.sin(ts_heading - math.pi)

        x_par = np.linspace(e_parx, e_startx, 20)
        y_par = np.linspace(e_pary, e_starty, 20)

        x = np.linspace(e_startx, e_endx, 40)
        y = np.linspace(e_starty, e_endy, 40)

        x_comb = np.concatenate((x,x_par)).reshape((60,1))
        y_comb = np.concatenate((y,y_par)).reshape((60,1))
        #plt.plot(x_comb,y_comb)
        #plt.plot(self.traj[0,:,0],self.traj[0,:,1])
        #plt.show()
        #print(np.hstack((x,y)))
        return np.hstack((x_comb,y_comb))


    def classifyCollision(self, obstacle_traj, ownship_traj): 
        #Try to just make it for rule 15 Give-way

        return("Give-way")



