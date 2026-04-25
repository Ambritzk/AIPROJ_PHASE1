# Example file showing a circle moving on screen
import pygame
import car
import road

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0



    




#This is just displays the road
rd = road.Road(screen)


#This is for allocating lanes
lanes = road.RoadWithLanes(x=screen.get_width() / 2,width=rd.rec_width * 0.98)
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


mc = car.Car(lanes.getLaneCenter(1),rd.rec_y + 500,30,50, "KEYS")

traffic = [car.Car(lanes.getLaneCenter(1),mc.y - 100,30,50,"DUMMY",mc,3)]
screen.fill("purple")
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    
    for traff in traffic:
        traff.Update(lanes.borders,[])


    mc.Update(lanes.borders,traffic)
    rd.Draw()
    lanes.draw(screen,mc.change)


    for i in traffic:
        i.Draw(screen)
    mc.Draw(screen)
    

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
