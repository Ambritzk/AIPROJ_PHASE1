import pygame
from utils import lerp

LenDash = 30
LenGap = 15


class Road:
    def __init__(self,screen):
        self.screen = screen
        self.rec_width = 300
        self.rec_height = screen.get_height()
        self.rec_x = ( screen.get_width() - self.rec_width ) / 2
        self.rec_y = 0
        self.rec = pygame.Rect(self.rec_x,self.rec_y,self.rec_width,self.rec_height)

    def getRoad(self):
        return self.rec
    
    def Draw(self):
        pygame.draw.rect(self.screen,"blue",self.rec)

class RoadWithLanes:
    def __init__(self,x,width,lanes = 3):
        self.x = x
        self.width = width
        self.lanes = lanes
        self.left = x - (width / 2)
        self.right = x + (width / 2)



        inf = 1000
        self.top = -inf
        self.bottom = inf


        topleft = {'x':self.left,'y':self.top}
        bottomleft = {'x':self.left,'y':self.bottom}
        topright = {'x':self.right,'y':self.top}
        bottomright = {'x':self.right,'y':self.bottom}

        self.borders = [[topleft,bottomleft], [topright,bottomright]]


        self.DashOrigin = -(LenDash + LenGap) + 15
        self.LaneOffset = 0
    def draw(self,screen,change):

        self.LaneOffset += change
        self.LaneOffset %= (LenDash + LenGap)

        starto = self.DashOrigin + self.LaneOffset
        for i in range(self.lanes + 1):
            lane_x = lerp(self.left,self.right,i / self.lanes)
            if i == 0 or i == self.lanes:
                pygame.draw.line(screen,'white',(lane_x,self.top),(lane_x,self.bottom),5)
                continue
            #pygame.draw.line(screen,"white",(lane_x,self.top),(lane_x,self.bottom),2)
            self.drawDashedLines(screen,starto,self.bottom,lane_x)
            
    def drawDashedLines(self,screen,start,end,x):
        lengthOfTheDash = LenDash
        lengthOfTheGap = LenGap
        totalpackage = lengthOfTheDash + lengthOfTheGap
        currentTop = start
        while currentTop < end:
            pygame.draw.line(screen,'white',(x,currentTop),(x,currentTop + lengthOfTheDash),5)
            currentTop += totalpackage
    

    def getLaneCenter(self,laneIndex):
        linewidth = self.width / self.lanes
        return self.left + linewidth / 2 + laneIndex * linewidth
    
