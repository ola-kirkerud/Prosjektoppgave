import math
import numpy as np

class OwnShip():


    def __init__(self, pos, traj, heading):
        self.pos = pos
        self.traj = traj
        self.heading = heading
        self.phi = 0
    
    def updatePos(self, delx, dely):
        #phi = math.atan(delx[math.floor(self.pos[0]),math.floor(self.pos[1])]/dely[math.floor(self.pos[0]),math.floor(self.pos[1])])
        #print(phi)
        #x = self.pos[0] + math.cos(phi)*0.1
        #y = self.pos[1] + math.sin(phi)*0.1

        delx_hat = delx[int(round(self.pos[0])),int(round(self.pos[1]))]/math.sqrt(delx[int(round(self.pos[0])),int(round(self.pos[1]))]**2+dely[int(round(self.pos[0])),int(round(self.pos[1]))]**2)
        dely_hat = dely[int(round(self.pos[0])),int(round(self.pos[1]))]/math.sqrt(delx[int(round(self.pos[0])),int(round(self.pos[1]))]**2+dely[int(round(self.pos[0])),int(round(self.pos[1]))]**2)

        if (delx[int(round(self.pos[0])),int(round(self.pos[1]))] == 0) and (delx[int(round(self.pos[0])),int(round(self.pos[1]))] == 0):
            phi = self.phi
            #print("Shit")
            #print(phi)
        else:
            phi = math.atan2(dely_hat, delx_hat)
            #print("YESS")
            #print(phi)

        if self.phi - phi > math.pi/400:
            phi = self.phi - math.pi/400
        elif self.phi - phi < -math.pi/400:
            phi = self.phi + math.pi/400


        self.phi = phi
        x = self.pos[0] + 0.066*math.cos(phi)
        y = self.pos[1] + 0.066*math.sin(phi)

        #print(x,y)

        #x = self.pos[0] + delx_hat*1
        #y = self.pos[1] + dely_hat*1

        self.pos = [x,y]

    def getPos(self):
        return self.pos

    def getGoal(self, t): 
        #use los guidence to find goal
        #check distance from ownship to traj
        #should also have a different one if the heading diff is to big 
        #must only look at the points that are ahead, not behind
        if t+500 >= self.traj.shape[0]:
            return self.traj[-1,:]
        else: 
            return self.traj[t+500,:]#self.traj[t+60]
    
    def updateHeading(self, old_pos):
        self.heading = np.arctan2(self.pos[1]-old_pos[1], self.pos[0]-old_pos[0])

    def getHeading(self):
        return self.heading