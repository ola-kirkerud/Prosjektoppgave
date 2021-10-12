class OwnShip():

    def __init__(self, pos, traj):
        self.pos = pos
        self.traj = traj
    
    def updatePos(self, pos):
        self.pos = pos
    
    def getPos(self):
        return self.pos

    def getGoal(self): 
        #use los guidence to find goal
        #check distance from ownship to traj
        #should also have a different one if the heading diff is to big 
        #must only look at the points that are ahead, not behind
