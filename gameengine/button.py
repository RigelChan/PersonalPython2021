import pygame


class Button:
        def __init__(self, width, height, sprites):
            self.width = width
            self.height = height
            self.sprites = sprites

        def isOver(self, pos, x, y):
            if pos[0] > x and pos[0] < x + self.width:
                if pos[1] > y and pos[1] < y + self.height:
                    return True
                
            return False

        def draw(self, screen, x, y):
            screen.blit(pygame.image.load(self.sprites[0]), (x, y))  # Drawing the button.

        def draw_activated(self, screen, x ,y):
            screen.blit(pygame.image.load(self.sprites[1]), (x, y))  # Drawing the activated version of the button.
