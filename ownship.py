import math
import numpy as np

class OwnShip():


    def __init__(self, pos, traj):
        self.pos = pos
        self.traj = traj
    
    def updatePos(self, delx, dely):
        #phi = math.atan(delx[math.floor(self.pos[0]),math.floor(self.pos[1])]/dely[math.floor(self.pos[0]),math.floor(self.pos[1])])
        #print(phi)
        #x = self.pos[0] + math.cos(phi)*0.1
        #y = self.pos[1] + math.sin(phi)*0.1

        delx_hat = delx[int(round(self.pos[0])),int(round(self.pos[1]))]/math.sqrt(delx[int(round(self.pos[0])),int(round(self.pos[1]))]**2+dely[int(round(self.pos[0])),int(round(self.pos[1]))]**2)
        dely_hat = dely[int(round(self.pos[0])),int(round(self.pos[1]))]/math.sqrt(delx[int(round(self.pos[0])),int(round(self.pos[1]))]**2+dely[int(round(self.pos[0])),int(round(self.pos[1]))]**2)

        #print("yes")
        #print(delx)
        x = self.pos[0] + delx_hat*1
        y = self.pos[1] + dely_hat*1

        self.pos = [x,y]

    def getPos(self):
        return self.pos

    def getGoal(self, t): 
        #use los guidence to find goal
        #check distance from ownship to traj
        #should also have a different one if the heading diff is to big 
        #must only look at the points that are ahead, not behind
        if t+30 >= self.traj.shape[0]:
            return self.traj[-1,:]
        else: 
            return self.traj[t+30]
