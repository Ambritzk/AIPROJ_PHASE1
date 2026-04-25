import math
from utils import lerp, getIntersection
import pygame
class Sensor:
    def __init__(self,car):
        self.car = car
        self.raycount = 15
        self.rayLength = 200
        self.raySpread = math.radians(45)

        self.rays = []
        self.readings = [] #for checking how far the borders are
    
    def Update(self,borders,traffic):
        self.CastRays()
        self.readings = []
        for ray in self.rays:
            self.readings.append(self.getReading(ray,borders,traffic))

    def getReading(self,ray,borders,traffic):
        #refer to lecture 3
        #we check for all possible collisions and choose the one closest
        touches = []
        for i in range(len(borders)):
            touch = getIntersection(ray[0],ray[1],borders[i][0],borders[i][1])
            if touch:
                touches.append(touch)

        #for traffic

        for i in range(len(traffic)):
            poly = traffic[i].polygon
            for j in range(len(poly)):
                value = getIntersection(ray[0],ray[1],poly[j],poly[(j + 1)%len(poly)])
                if value:
                    touches.append(value)
        if len(touches) == 0:
            return None
        else:
            offsets = [x.get('offset') for x in touches]
            minoffset = min(offsets)
            return [tch for tch in touches if tch['offset'] == minoffset]
             

    def CastRays(self):
        self.rays = []
        for i in range(self.raycount):
            rayAngle = lerp(self.raySpread / 2,-self.raySpread / 2,i/(self.raycount - 1) if self.raycount != 1 else 0.5) + math.radians(self.car.angle)
            #car.angle makes the sensor rays rotate
            #0.5 if raycount is 1

            start = {'x':self.car.x,'y':self.car.y}
            end = {
                'x':self.car.x - math.sin(rayAngle)*self.rayLength,
                'y':self.car.y-math.cos(rayAngle)*self.rayLength   }

            self.rays.append([start,end])
    
    def Draw(self,screen):
        for i in range(self.raycount):
            tail = self.rays[i][1]
            if i < len(self.readings) and self.readings[i] is not None:
                tail = self.readings[i][0]


            pygame.draw.line(screen,"black",(self.rays[i][1]['x'],self.rays[i][1]['y']),(tail['x'],tail['y']),3)
            pygame.draw.line(screen,"yellow",(self.rays[i][0]['x'],self.rays[i][0]['y']),(tail['x'],tail['y']),3)

            
