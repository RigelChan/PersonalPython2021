import pygame
import sys
import time
import ctypes
import os
from constants import Constants
from graphics import Graphics
from scenes import MainMenu
from utils import SceneManager
ctypes.windll.user32.SetProcessDPIAware()  # Makes the window the correct size irrelevant of Windows 10 scale settings. Doesn't apply
# here for obvious reasons.

class Game:
    def __init__(self):
        self.c = Constants()
        self.g = Graphics()
        self.sm = SceneManager()
        
        pygame.init()
        pygame.mixer.pre_init(frequency=44100, size=16, channels=2, buffer=312)
        
        self.dt = 0

        # Doublebuf makes use of a better memory management, thus it will increase performance.
        self.screen = pygame.display.set_mode((self.c.screen_width, self.c.screen_height), pygame.RESIZABLE, pygame.DOUBLEBUF, vsync=1) 
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Game")
        self.window_icon = pygame.image.load(self.g.icon)
        pygame.display.set_icon(self.window_icon)
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.last_time = time.time()

        self.mm = MainMenu()
        self.sm.push(self.mm) # Pushing here makes sure the object types are consistent.

    def draw_screen(self):
        self.sm.draw(self.screen)

    def check_events(self):
        self.sm.input(self)

    def update(self):
        self.sm.update(self.dt)

    def run(self):
        while True:
            self.check_events()
            self.draw_screen()
            self.update()
            self.dt = self.clock.tick(60)/1000


if __name__ == "__main__":
    g = Game()
    g.run()
