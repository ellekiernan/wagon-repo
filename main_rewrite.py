import pygame
import random
import time
import os, sys
from pygame.locals import *

#TODO Define classes for each object with sprites

pygame.init()
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
image_path = "/Users/elle/repositories/wagon-repo/images/"
white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 200)


def load_images(path):
    images = []
    image_directory = os.listdir(path)
    image_directory.sort()
    for png in image_directory:
        image = pygame.image.load(path + png).convert_alpha()
        image = pygame.transform.scale(image, (128, 256))
        images.append(image)
        #Make images auto scale to correct size
    return images


class Cactus():
    pass

class HorseDrugs(pygame.sprite.Sprite):
    def __init__(self, x = random.randrange(0, display_width), y = -300, width = 50, images = [], speed = 5):
        super().__init__(all_sprites)
        self.images = images
        self.image = images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        pass
    
    def move(self):
        pass


class Player(pygame.sprite.Sprite):
    def __init__(self, x = 0.5 * display_width, y = 0.6 * display_height, width = 50, images = [], speed = 10):
        super().__init__(all_sprites)
        self.images = images
        self.image = images[0]
        self.rect = self.image.get_rect()
        self.width = width
        self.rect.x = x
        self.rect.y = y

    def update(self):
        pressed = pygame.key.get_pressed()

        up, down, left, right = [pressed[key] for key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)]
        if up:
            self.y_change = -4
        elif down:
            self.y_change = 10
        else:
            self.y_change = 0
        if right:
            self.x_change = 8
        elif left:
            self.x_change = -8
        else:
            self.x_change = 0
        
        self.rect.x += self.x_change
        self.rect.y += self.y_change


#load images for things in gameLoop
player_images = load_images(image_path + "wagon/")
drug_images = load_images(image_path + "GOODhorsedrugs/")

#create sprite groups for sprites in gameLoop
player_group = pygame.sprite.RenderUpdates()
cactus_group = pygame.sprite.RenderUpdates()
drug_group = pygame.sprite.RenderUpdates()
all_sprites = pygame.sprite.RenderUpdates()

#initialize the sprites
player = Player(0.5 * display_width, 0.7 * display_height, 50, player_images, 10)
horse_drugs = HorseDrugs(images = drug_images)

#add sprites to non all_sprites groups (sprites initialized in super().init() to be in all_sprites)
player.add(player_group)

def gameLoop():

    gameExit = False
    gameDisplay.fill(white)

    while not gameExit:

        if pygame.event.peek(pygame.QUIT) == True:
            gameExit = True

        all_sprites.update()

        pygame.display.update(all_sprites.draw(gameDisplay))
        clock.tick(30)


gameLoop()
pygame.display.quit()
pygame.quit()