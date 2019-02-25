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
    def __init__(self, x = 0.5 * display_width, y = 0.6 * display_height, width = 50, images = [], speed = 10):
        super().__init__(all_sprites)
        self.images = images
        self.image = images[0]
        print(type(images[0]))
        self.rect = self.image.get_rect()
        self.width = width
        self.rect.x = x
        self.rect.y = y

    def update(self, pressed):
        pass

    def movePlayer(self):
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

        player.movePlayer()

        pygame.display.update(all_sprites.draw(gameDisplay))
        clock.tick(30)


gameLoop()
pygame.display.quit()
pygame.quit()