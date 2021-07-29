import pygame
import sys
import utils
import json
from savestates import Savestates
from constants import Constants
from variables import Variables
from entity import Collectible, DamagePickup, HealthPickup, Player
from button import Button
from graphics import Graphics


class Scene: #  This is the abstract class we base all other scenes upon.
    def __init__(self):
        pass
    def update(self, sm, dt):
        pass
    def enter(self):
        pass
    def exit(self):
        pass
    def input(self, sm):
        pass
    def draw(self, sm, screen):
        pass

class MainMenu(Scene):
    def __init__(self):
        self.c = Constants()
        self.g = Graphics()
        self.pos = (0,0)
        
        self.play_button = Button(200, 75, self.g.play_button)
        self.settings_button = Button(200, 75, self.g.settings_button)
        self.exit_button = Button(200, 75, self.g.exit_button)

    def draw(self, sm, screen): # We pass in sm referring to its instance within the scene manager.
        screen.fill(self.c.black)
        
        screen.blit(pygame.image.load(self.g.title), (screen.get_width()/2-450, screen.get_height()/24)) #python3 main.py
        
        if self.play_button.isOver(self.pos, screen.get_width()/2-100, screen.get_height()/3):
            self.play_button.draw_activated(screen, screen.get_width()/2-100, screen.get_height()/3)
        else:
            self.play_button.draw(screen, screen.get_width()/2-100, screen.get_height()/3)
            
        if self.settings_button.isOver(self.pos, screen.get_width()/2-100, screen.get_height()/2):
            self.settings_button.draw_activated(screen, screen.get_width()/2-100, screen.get_height()/2)
        else:
            self.settings_button.draw(screen, screen.get_width()/2-100, screen.get_height()/2) 
            
        if self.exit_button.isOver(self.pos, screen.get_width()/2-100, screen.get_height()/1.5):
            self.exit_button.draw_activated(screen, screen.get_width()/2-100, screen.get_height()/1.5)
        else:
            self.exit_button.draw(screen, screen.get_width()/2-100, screen.get_height()/1.5)         
 
    def update(self, sm, dt):
        pass
        
    def input(self, sm, instance):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    sm.push(FadeTransitionScene(self, Game()))
                if event.key == pygame.K_s:
                    sm.push(FadeTransitionScene(self, SettingsMenu()))
                if event.key == pygame.K_q:
                    sys.exit(0)
            if event.type == pygame.MOUSEMOTION:
                self.pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.pos = pygame.mouse.get_pos()
                if self.play_button.isOver(self.pos, instance.screen.get_width()/2-100, instance.screen.get_height()/3):
                    sm.push(FadeTransitionScene(self, Game()))
                if self.settings_button.isOver(self.pos, instance.screen.get_width()/2-100, instance.screen.get_height()/2):
                    sm.push(FadeTransitionScene(self, SettingsMenu()))
                if self.exit_button.isOver(self.pos, instance.screen.get_width()/2-100, instance.screen.get_height()/1.5):
                    sys.exit(0)
            if event.type == pygame.VIDEORESIZE:
                instance.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE, pygame.DOUBLEBUF, vsync=1)
                    
    def exit(self):
        print("Leaving Main Menu.")
        
    def enter(self):
        print("Entering Main Menu.")

class Game(Scene):
    def __init__(self):
        self.c = Constants()
        self.g = Graphics()
        self.save = Savestates()
        self.save.open_save()
        self.player = Player(self.save.data["player"][0], self.save.data["player"][1], 300)
        self.player.health = self.save.data["player"][2]
        self.player.points = self.save.data["player"][3]

        self.collectible_dict = {}
        self.object_dict = {}

        self.temp_value = 0

        for i in self.save.data["collectibles"]:
            name = 'obj_{}'.format(self.temp_value)
            self.collectible_dict.update({name: i})

            self.temp_value += 1

        for i in self.collectible_dict:
            if self.collectible_dict[i][0] == "generic":
                self.object_dict[i] = self.object_dict.get(i, Collectible(self.collectible_dict[i][1], self.collectible_dict[i][2]))
            if self.collectible_dict[i][0] == "health":
                self.object_dict[i] = self.object_dict.get(i, HealthPickup(self.collectible_dict[i][1], self.collectible_dict[i][2]))
            if self.collectible_dict[i][0] == "damage":
                self.object_dict[i] = self.object_dict.get(i, DamagePickup(self.collectible_dict[i][1], self.collectible_dict[i][2]))

        self.final_list = list(self.object_dict.values())
        self.save_list = []

    def draw(self, sm, screen):
        screen.fill(self.c.black)
        self.player.draw(screen)

        for i in range(len(self.final_list)):
            self.final_list[i].draw(screen)

        screen.blit(pygame.image.load(self.g.stats), (0, 0))
        utils.draw_text(screen, str(self.player.points), "assets/dogica.ttf", size=20, pos=(155,155))
        pygame.draw.rect(screen, (255, 255, 255), (155, 22, self.player.health, 21))

    def input(self, sm, instance):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_data()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    sm.pop()
                    sm.push(FadeTransitionScene(self, None)) # We pass none as we are not transitiong to a *new* scene.
                    self.save_data()
                if event.key == pygame.K_w:
                    self.player.moving_up = True
                elif event.key == pygame.K_s:
                    self.player.moving_down = True
                elif event.key == pygame.K_a:
                    self.player.moving_left = True
                elif event.key == pygame.K_d:
                    self.player.moving_right = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.player.moving_up = False
                elif event.key == pygame.K_s:
                    self.player.moving_down = False
                elif event.key == pygame.K_a:
                    self.player.moving_left = False
                elif event.key == pygame.K_d:
                    self.player.moving_right = False
            if event.type == pygame.VIDEORESIZE:
                instance.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE, pygame.DOUBLEBUF, vsync=1)
            
                                
    def update(self, sm, dt):
        self.player.update(dt)        
        for item in self.final_list:
            if self.player.player_rect.colliderect(item.rect):
                if item.name == "health" and self.player.health < 723:
                    self.player.health += 50
                elif item.name == "damage":
                    self.player.health -= 100
                 
                self.final_list.remove(item)
                self.player.points += 1
                

    def exit(self):
        print("Leaving Game.")
    
    def enter(self):
        print("Entering Game.")

    def save_data(self):
        self.save.data["player"][0], self.save.data["player"][1] = int(self.player.x), int(self.player.y)
        self.save.data["player"][2] = self.player.health
        self.save.data["player"][3] = self.player.points
        
        for i in self.final_list:
            temp = [i.name, i.x, i.y]
            self.save_list.append(temp)

        self.save.data["collectibles"] = self.save_list

        self.save.close_save() # Saving the player's position when we go back to the main menu.

class SettingsMenu(Scene):
    def __init__(self):
        self.c = Constants()
        self.v = Variables()
        self.monitor_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        
    def draw(self, sm, screen):
        screen.fill(self.c.black)
        utils.debug_text(screen, "Game: [M] to Menu")
        utils.debug_text(screen, "Click [F] to toggle Fullscreen", pos=(20, 300))
        
    def input(self, sm, instance):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    sm.pop()
                    sm.push(FadeTransitionScene(self, None))
                if event.key == pygame.K_f:
                    self.v.fullscreen = not self.v.fullscreen
                    if self.v.fullscreen:
                        pygame.display.set_mode(self.monitor_size, pygame.FULLSCREEN)
                    else:
                        pygame.display.set_mode((self.c.screen_width, self.c.screen_height), pygame.RESIZABLE)
            if event.type == pygame.VIDEORESIZE:
                instance.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE, pygame.DOUBLEBUF, vsync=1)
                    
    def exit(self):
        print("Leaving Settings.")
    
    def enter(self):
        print("Entering Settings.")

class TransitionScene(Scene):
    def __init__(self, fromScene, toScene):
        self.c = Constants()
        self.currentPercentage = 0
        self.fromScene = fromScene
        self.toScene = toScene
    def update(self, sm, dt):
        self.currentPercentage += 4
        if self.currentPercentage >= 100:
            sm.pop() # Pops itself when the transition is finished.
            if self.toScene is not None:
                sm.push(self.toScene) # Pushes the next scene onto the stack and displays it.
                
    def exit(self):
        print("Leaving Transition.")
    
    def enter(self):
        print("Entering Transition.")

    def input(self, sm, instance):
        pass

class FadeTransitionScene(TransitionScene):
    def draw(self, sm, screen):
        if self.currentPercentage < 50:
            self.fromScene.draw(sm, screen) # Draw the old scene while transition is only half way complete.
        else:
            if self.toScene is None:
                sm.scenes[-2].draw(sm, screen)
            else:
                self.toScene.draw(sm, screen)
        
        alpha = 255 - int(abs((255-(255/50)*self.currentPercentage))) # Subtact 510 from 255, and then return an abs value.
        overlay = pygame.Surface((self.c.screen_width, self.c.screen_height))
        overlay.set_alpha(alpha)
        overlay.fill(self.c.black)
        screen.blit(overlay, (0,0))

