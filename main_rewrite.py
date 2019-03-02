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
image_path = "/Users/elle/repos/wagon-repo/images/"
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
        size = image.get_rect().size
        image = pygame.transform.scale(image, (5 * size[0], 5 * size[1]))
        images.append(image)
        #Make images auto scale to correct size
    return images


class Cactus(pygame.sprite.Sprite):
    def __init__(self, x = random.randrange(0, display_width), y = -300, width = 50, images = [], speed = 5):
        super().__init__(all_sprites, cactus_group)
        self.images = images
        self.image = images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.speed = speed
        

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > display_height:
            self.rect.y = -random.randrange(10, 100)
            self.rect.x = random.randrange(0, display_width)

            player.dodged_cactuses += 1

            if len(cactus_group.sprites()) < 10:
                new_cactus = Cactus(images = cactus1_images)
            

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

class Player(pygame.sprite.Sprite):
    def __init__(self, x = 0.5 * display_width, y = 0.6 * display_height, width = 50, images = [], speed = 10):
        super().__init__(all_sprites)
        self.images = images
        self.image = images[0]
        self.rect = self.image.get_rect()
        self.width = width
        self.rect.centerx = x
        self.rect.centery = y

        self.dodged_cactuses = 0
        self.drug_count = 0
        self.drugged = False

    def update(self):
        pressed = pygame.key.get_pressed()

        up, down, left, right, space = [pressed[key] for key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_SPACE)]


        if up and self.rect.centery > 0:
            self.y_change = -4
        elif down and self.rect.centery < display_height:
            self.y_change = 10
        else:
            self.y_change = 0
        if right and self.rect.centerx  < display_width:
            self.x_change = 8
        elif left and self.rect.centerx > 0:
            self.x_change = -8
        else:
            self.x_change = 0
        
        if space and self.drug_count != 0 and self.drugged == False:
            self.drug_count -= 1
            self.drugged = True
            pygame.time.set_timer(USEREVENT, 5000)



        self.rect.centerx += self.x_change
        self.rect.centery += self.y_change

class boostIcon(pygame.sprite.Sprite):
    def __init__(self, x = 0.0001 * display_width, y = 0.01 * display_height, images = []):
        super().__init__(all_sprites)
        
        self.images = images
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        if player.drug_count < 5:
            self.image = self.images[player.drug_count]

class Background():
    def __init__(self, image):

        self.y1 = 0
        self.image = image
        self.y2 = -display_height

    def update(self):
        if self.y1 > display_height:
            self.y1 = -display_height + 5
        if self.y2 > display_height:
            self.y2 = -display_height + 5
        self.y1 += 5
        self.y2 += 5
        
    
    def render(self):
        gameDisplay.blit(self.image, (0, self.y1))
        gameDisplay.blit(self.image, (0, self.y2))

def generic_text(text, size, color, text_center):
        font = pygame.font.Font("freesansbold.ttf", size)
        rendered_text = font.render(text, True, color)
        gameDisplay.blit(rendered_text, rendered_text.get_rect(center = text_center))

def crash():
    gameExit = True
    pygame.display.quit()
    pygame.quit()

#load images for things in gameLoop
player_images = load_images(image_path + "wagon/")
drug_images = load_images(image_path + "GOODhorsedrugs/")
cactus1_images = load_images(image_path + "cactus1/")
cactus2_images = load_images(image_path + "cactus2/")
cactus_images = cactus1_images + cactus2_images
boost_icon_images = load_images(image_path + "boost_icon/")
number_images = load_images(image_path + "numbers/")

bg_image = pygame.image.load("/Users/elle/repos/wagon-repo/images/background/background0.png").convert_alpha()
bg_size = bg_image.get_rect().size
bg_image = pygame.transform.scale(bg_image, (5 * bg_size[0], 5 * bg_size[1]))


#create sprite groups for sprites in gameLoop
player_group = pygame.sprite.RenderUpdates()
cactus_group = pygame.sprite.RenderUpdates()
drug_group = pygame.sprite.RenderUpdates()
all_sprites = pygame.sprite.RenderUpdates()
hud_group = pygame.sprite.RenderUpdates()


#initialize the sprites
player = Player(0.5 * display_width, 0.7 * display_height, 50, player_images, 10)
horse_drugs = HorseDrugs(images = drug_images)
cactus = Cactus(images = cactus1_images)
boost_icon = boostIcon(images = boost_icon_images)

#initialize the background
bg = Background(image = bg_image)


#add sprites to non all_sprites groups (sprites initialized in super().init() to be in all_sprites)
player.add(player_group)
cactus.add(cactus_group)
horse_drugs.add(drug_group)


def gameLoop():
    gameExit = False

    while not gameExit:
        gameDisplay.fill(white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == USEREVENT:
                player.drugged = False
                pygame.time.set_timer(USEREVENT, 0)


        if pygame.sprite.spritecollide(player, cactus_group, False) and player.drugged == False:
            gameExit = True

        if pygame.sprite.spritecollide(player, drug_group, False):
            horse_drugs.rect.y = -random.randrange(100, 1400)
            if player.drug_count < 5:
                player.drug_count += 1

        all_sprites.update()
        bg.render()
        bg.update()

        generic_text(str(player.dodged_cactuses), 40, black, (0.04 * display_width, 0.1 * display_height))


        pygame.display.update(all_sprites.draw(gameDisplay))
        
        clock.tick(60)


gameLoop()
pygame.display.quit()
pygame.quit()