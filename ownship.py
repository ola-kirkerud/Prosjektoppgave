import math
import numpy as np

class OwnShip():


    def __init__(self, pos, traj):
        self.pos = pos
        self.traj = traj
    
    def updatePos(self, delx, dely):
        x = self.pos[0] + dely[math.floor(self.pos[0]),math.floor(self.pos[1])] / 100
        y = self.pos[1] + delx[math.floor(self.pos[0]),math.floor(self.pos[1])] / 100

        print(delx[math.floor(self.pos[0]),math.floor(self.pos[1])], dely[math.floor(self.pos[0]),math.floor(self.pos[1])])

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
