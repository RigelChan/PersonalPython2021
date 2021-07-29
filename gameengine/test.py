import sys
 
import pygame
from utils import SpriteSheet
 
pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
star_png = pygame.image.load("assets/star.png").convert()

star_spritesheet = SpriteSheet(star_png)

# Star Sprites
star_0 = star_spritesheet.get_image(0, 200, 200, 1, (255,255,255))
star_1 = star_spritesheet.get_image(1, 200, 200, 1, (255,255,255))
star_2 = star_spritesheet.get_image(2, 200, 200, 1, (255,255,255))
star_3 = star_spritesheet.get_image(3, 200, 200, 1, (255,255,255))

sprite_list = [star_0, star_1, star_2, star_3]

i = 0
timer = 0
animation_clock = 10

# Game loop.
while True:
    screen.fill((0, 0, 0))
    
    
    screen.blit(sprite_list[i], (0,0))
  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
  
    # Update.

    if timer < animation_clock:

        timer += 1

    elif timer >= animation_clock:

        if i < 3:
            i += 1
        else:
            i = 0

        timer = 0

    print(timer)

    # Draw.

    pygame.display.update()
    fpsClock.tick(fps)