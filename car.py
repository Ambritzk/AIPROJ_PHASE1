import pygame
import math
import utils
from network import NeuralNetwork
from sensor import Sensor

class Car:
    def __init__(self,x,y,width,height, controlType, referenceToTheMainCar = None, maxspeed = 10):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.tempy = self.y

        self.left = False
        self.right = False
        self.forward = False
        self.reverse = False

        self.speed = 0
        self.acceleration = 0.2
        self.maxspeed = maxspeed
        self.friction = 0.05
        self.angle = 0

        self.useBrain = (controlType == "AI")
        self.change = 0 #for updating the environment wrt to the mc

        if controlType != 'DUMMY':
            self.sensor = Sensor(self)
            self.brain = NeuralNetwork([self.sensor.raycount,6,4])

        self.damaged = False
        self.controlType = controlType
        if self.controlType == "DUMMY":
            self.forward = True


        self.RefTomc: Car = referenceToTheMainCar #This is for the traffic cars to move according to the main car


    def Update(self,borders,traffic):
        if self.controlType == 'KEYS':
            self.HandleInput()
        


        if not self.damaged:
            self.Move()
            if self.controlType == 'DUMMY':
                self.DummyControls()
            self.polygon = self.CreatePolygon()
            self.damaged = self.assessDamage(borders,traffic) 
        else:
            self.change = 0

        if self.controlType != 'DUMMY':
            self.sensor.Update(borders,traffic)
            offsets = [1 - reading[0]['offset'] if reading is not None else 0 for reading in self.sensor.readings]
            
            outputs = NeuralNetwork.feedForward(offsets,self.brain)
            print(outputs)

            if self.useBrain:
                self.forward = outputs[0]
                self.left = outputs[1]
                self.right = outputs[2]
                self.reverse = outputs[3]


    def Draw(self,screen):
        # screen.blit(self.rotated,self.finalcar.topleft)
        color = "black" if self.controlType in ['KEYS','AI'] else "red"
        if self.damaged:
            color = "gray"
        pairs = [(p.get('x'),p.get('y')) for p in self.polygon]
        pygame.draw.polygon(screen,color,pairs)
        if self.controlType == 'KEYS':
            self.sensor.Draw(screen)

    def CreatePolygon(self):
        points = []
        rad = math.hypot(self.width,self.height) / 2
        alpha = math.atan2(self.width,self.height)

        ang = math.radians(self.angle)
        
        points.append({'x':self.x - math.sin(ang - alpha) * rad,
                       'y':self.y - math.cos(ang - alpha) * rad})


        points.append({'x':self.x - math.sin(ang + alpha) * rad,
                       'y':self.y - math.cos(ang + alpha) * rad})
        
        points.append({'x':self.x - math.sin(math.pi + ang - alpha) * rad,
                       'y':self.y - math.cos(math.pi + ang - alpha) * rad})
                       
        points.append({'x':self.x - math.sin(math.pi + ang + alpha) * rad,
                       'y':self.y - math.cos(math.pi + ang + alpha) * rad})
        
        return points
    
    
    def HandleInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.forward = True
        else:
            self.forward = False
        
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.reverse = True
        else:
            self.reverse = False
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.left = True
        else:
            self.left = False

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.right = True
        else:
            self.right = False




    




    def Move(self):
        if self.forward:
            self.speed += self.acceleration
        elif self.reverse:
            self.speed -= self.acceleration
        
        if self.speed > self.maxspeed:
            self.speed = self.maxspeed
        
        if self.speed < -self.maxspeed / 2:
            self.speed = -self.maxspeed / 2
        
        if self.speed > 0:
            self.speed -= self.friction
        elif self.speed < 0:
            self.speed += self.friction
        
        if abs(self.speed) < self.friction:
            self.speed = 0

        ang = 1.5
        if self.left:
            if self.reverse:
                self.angle -= ang
            else:
                self.angle += 1.5
        if self.right:
            if self.reverse:
                self.angle += ang 
            else:
                self.angle -= 1.5

        #self.y -= self.speed

        rad = math.radians(self.angle)
        self.x -= math.sin(rad) * self.speed

        old_y = self.tempy #for the dash illusion
        self.tempy -= math.cos(rad) * self.speed


        self.change = -(self.tempy - old_y)


    def assessDamage(self,borders,traffic):
        for i in range(len(borders)):
            if utils.polysIntersect(self.polygon,borders[i]):
                return True
        
        for i in range(len(traffic)):
            if utils.polysIntersect(self.polygon,traffic[i].polygon):
                return True
        
        return False
    


    def DummyControls(self):
        mc = self.RefTomc


        if abs(abs(self.y) - abs(mc.y)) > 2 * 720:
            if self.y > mc.y:
                self.y = -335
            else:
                self.y = 720 + 335


        if self.change > mc.change:
            self.y -= (self.change - mc.change)
        else:
            self.y += (mc.change - self.change)



