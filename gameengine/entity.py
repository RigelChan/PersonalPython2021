import pygame
from graphics import Graphics


class Entity:
    def __init__(self):
        pass

    def draw(self, screen):
        pass
        
    def update(self, dt=1):
        pass
    
    def input(self):
        pass
    
class Player(Entity):
    def __init__(self, x, y, speed):
        self.g = Graphics()
        self.x = x
        self.y = y

        self.points = 0
        self.health = 723
        
        self.sprite = pygame.image.load(self.g.player)
        self.player_rect = self.sprite.get_rect(center=(self.x+50,self.y+50))
        
        self.moving_up = False
        self.moving_left = False
        self.moving_right = False
        self.moving_down = False

        self.speed = speed
        
    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))
        #pygame.draw.rect(screen, (255, 0, 0), self.player_rect) - debug square
        
    def update(self, dt):
        self.player_rect = self.sprite.get_rect(center=(self.x+50,self.y+50))
        if self.moving_up:
            self.y -= self.speed * dt
        if self.moving_left:
            self.x -= self.speed * dt
        if self.moving_down:
            self.y += self.speed * dt
        if self.moving_right:
            self.x += self.speed * dt

class Collectible(Entity):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        # self.type = None
        self.name = "generic"
        
    def draw(self, screen):
        pygame.draw.rect(screen, (255,255,255), (self.x, self.y, 20, 20))

class HealthPickup(Entity):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 10, 10)
        # self.type = "good"
        self.name = "health"

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, 10, 10))

class DamagePickup(Entity):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, 30, 30)
        # self.type = "bad"
        self.name = "damage"

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 30, 30)) 
