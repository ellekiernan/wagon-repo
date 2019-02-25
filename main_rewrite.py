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

class HorseDrugs():
    pass

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, images, speed):
        super().__init__(all_sprites)
        self.images = images
        self.image = images[0]
        print(type(images[0]))
        self.rect = self.image.get_rect()
        self.width = width
        self.rect.x =  0.5 * display_width
        self.rect.y = 0.7 * display_height

    def update(self, pressed):
        pass

path = "/Users/elle/repositories/wagon-repo/images/"
player_images = load_images(path + "wagon/")
all_sprites = pygame.sprite.RenderUpdates()
player_group = pygame.sprite.RenderUpdates()
player = Player(0.5 * display_width, 0.7 * display_height, 50, player_images, 10)
player.add(player_group, all_sprites)

def gameLoop():

    gameExit = False
    gameDisplay.fill(white)

    while not gameExit:

        if pygame.event.peek(pygame.QUIT) == True:
            gameExit = True

        pygame.display.update(all_sprites.draw(gameDisplay))
        clock.tick(30)


gameLoop()
pygame.display,quit()
pygame.quit()
quit()