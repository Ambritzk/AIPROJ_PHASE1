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



    


def getRoad():
    rec_width = screen.get_width() / 2
    rec_height = screen.get_height()
    rec_x = ( screen.get_width() - rec_width ) / 2
    rec_y = 0
    rec = pygame.Rect(rec_x,rec_y,rec_width,rec_height)
    return rec

rd = road.Road(screen)



lanes = road.RoadWithLanes(x=screen.get_width() / 2,width=rd.rec_width * 0.98)
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


mc = car.Car(lanes.getLaneCenter(1),rd.rec_y + 500,30,50)
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    #pygame.draw.circle(screen, "red", player_pos, 40)
    mc.HandleInput()
    change = mc.Update(lanes.borders)
    rd.Draw()
    lanes.draw(screen,change)

    mc.y = screen.get_height() // 2  + (screen.get_height() // 4)
    mc.Draw(screen)
    

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()
