import pygame
import sys
import ctypes


ctypes.windll.user32.SetProcessDPIAware()

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.pre_init(frequency=44100, size=16, channels=2, buffer=312)
        self.window = pygame.display.set_mode((1920, 1080), vsync=1)
        self.string = """In this world, it is kill or be killed dearie... Now, give your soul to me, or all shall perish."""
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("PixelFont.ttf", 40)
        self.draw_string = ""
        self.text_counter = 0
        self.i = 0
        self.x = 0
        self.text_x = 540
        self.text_y = 620
        self.blip = pygame.mixer.Sound("blip.wav")
        self.blip.set_volume(0.05)
        self.box = "box.png"
        self.box_width = 737
        self.complete = False
        self.char_limit = 65

        self.char_array = []
        self.surface_array = []

        self.box_surface = pygame.Surface((737, 300))
 
# Secondary Functions.

    def _draw_text(self, message, pos):
        x = pos[0]
        y = pos[1]
        if self.i < len(message): # Checking if we've completed the sentence.
            for i in range(0, len(message)): # Looping through the sentence.
                if self.text_counter > 1:
                    self.draw_string += message[self.i]  # Appending more of the message to the draw string.
                    self.text_counter = 0
                    self.i += 1
                    
        
        word_surface = self.font.render(self.draw_string, True, (255, 255, 255))

        if word_surface.get_width() >= self.box_width:
            x = pos[0]
            y += 50
        self.window.blit(word_surface, (x, y))

        print(self.text_counter) 

    def _draw_text_final(self):
        if self.i < len(self.string):
            for char in self.string:
                self.char_array.append(char)

            for char in self.char_array:
                self.surface_array.append(self.font.render(char, True, (255, 255, 255)))
                self.i += 1

        if self.text_counter == 2 and self.x < len(self.surface_array):
            #self.blip.play()
            if self.x < 38:       
                self.box_surface.blit(self.surface_array[self.x], (0 + self.x * self.surface_array[0].get_width(), 0))
                self.x += 1
                self.text_counter = 0

            elif 38 <= self.x < 76:
                self.box_surface.blit(self.surface_array[self.x], (0 + self.x * self.surface_array[0].get_width() - 722, 30))
                self.x += 1
                self.text_counter = 0

            elif 76 <= self.x < 114:
                self.box_surface.blit(self.surface_array[self.x], (0 + self.x * self.surface_array[0].get_width() - 722 * 2, 60))
                self.x += 1
                self.text_counter = 0

            elif 114 <= self.x < 152:
                self.box_surface.blit(self.surface_array[self.x], (0 + self.x * self.surface_array[0].get_width() - 722 * 3, 90))
                self.x += 1
                self.text_counter = 0

        self.window.blit(self.box_surface, (540,610))
        
    def _draw_text_box(self):
        self.window.blit(pygame.image.load(self.box), (520, 590))
                                    
# Core Functions.  
         
    def draw(self):
        self.window.fill((0,0,0))
        #self._draw_text(self.string, (540, 610))
        self._draw_text_final()
        self._draw_text_box()
        # pygame.draw.rect(self.window, (255,0,0), pygame.Rect(540, 610, 737, 192))
        pygame.display.update()
        
    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
                
    def update(self):
        self.text_counter += 1
    
    def run(self):
        while True:
            self.update()
            self.input()
            self.draw()
            self.clock.tick(60)
            
game = Game()
game.run()
        