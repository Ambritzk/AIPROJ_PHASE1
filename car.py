import pygame
import math
import utils
from sensor import Sensor

class Car:
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.left = False
        self.right = False
        self.forward = False
        self.reverse = False

        self.speed = 0
        self.acceleration = 0.2
        self.maxspeed = 3
        self.friction = 0.05
        self.angle = 0
        self.car_rect = pygame.Surface((self.width,self.height),pygame.SRCALPHA)
        self.car_rect.fill("white")

        self.sensor = Sensor(self)


        self.damaged = False


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
    


    def Update(self,borders):
        change = 0
        if not self.damaged:
            change = self.Move()
            self.polygon = self.CreatePolygon()
            self.damaged = self.assessDamage(borders)
        self.sensor.Update(borders)
        return change



    def Draw(self,screen):
        # screen.blit(self.rotated,self.finalcar.topleft)
        color = "black"
        if self.damaged:
            color = "gray"
        pairs = [(p.get('x'),p.get('y')) for p in self.polygon]
        pygame.draw.polygon(screen,color,pairs)
        self.sensor.Draw(screen)


    
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



        self.rotated = pygame.transform.rotate(self.car_rect,self.angle)
        self.finalcar = self.rotated.get_rect(center = (self.x,self.y))
    




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

        old_y = self.y #for the dash illusion
        self.y -= math.cos(rad) * self.speed


        return -(self.y - old_y)


    def assessDamage(self,borders):
        for i in range(len(borders)):
            if utils.polysIntersect(self.polygon,borders[i]):
                return True
        
        return False
    
