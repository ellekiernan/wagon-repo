import pygame
from pygame.locals import *
import time
import random
import os, sys

pygame.init()

display_width = 1024
display_height = 1024

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("A Bit Racey")

black = (0, 0, 0)
white = (255, 255, 255)
red = (200, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 200)
bright_red = (255, 0, 0)
bright_green = (0, 255, 0)
bright_blue = (0, 0, 255)


wagonpng = pygame.image.load("/Users/elle/pygameImages/wagon.png")
wagonpng = pygame.transform.scale(wagonpng, (128, 256))
cactuspng = pygame.image.load("/Users/elle/pygameImages/cactus1.png")
cactuspng = pygame.transform.scale(cactuspng, (128, 128))

clock = pygame.time.Clock()

def loadImages(path):
    images = []
    for png in os.listdir(path):
        image = pygame.image.load(path + png).convert_alpha()
        size = image.get_rect().size
        image = pygame.transform.scale(image, (5*size[0], 5*size[1]))
        images.append(image)
    return images, size

boost_images, boost_images_size = loadImages("/Users/elle/wagongame/GOODhorsedrugs/")
wagon_images, wagon_images_size = loadImages("/Users/elle/wagongame/wagon/")
cactus1_images, cactus1_images_size = loadImages("/Users/elle/wagongame/cactus1/")
cactus2_images, cactus2_images_size = loadImages("/Users/elle/wagongame/cactus2/")
rock_images, rock_images_size = loadImages("/Users/elle/wagongame/rock/")



class obstacle:
    def __init__(self, x, y, w, h, speed, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.speed = speed
        self.color = color

    def draw(self):
        gameDisplay.blit(cactuspng, (self.x, self.y))
        pygame.draw.rect(gameDisplay, self.color, [self.x, self.y, self.w, self.h])

class cactus(pygame.sprite.Sprite):
    def __init__(self, x, y, size, image, speed):
        pygame.sprite.Sprite.__init__(self)

        self.x = x
        self.y = y
        self.speed = speed
        self.size = size
        self.rect = pygame.Rect((x, y), (self.size))
        self.rect.x = x
        self.rect.y = y
        self.image = image
        
        def update(self):
            self.y += self.speed

class boost(pygame.sprite.Sprite):
    def __init__(self, x, y, size, images, speed):
        pygame.sprite.Sprite.__init__(self)
    
        self.speed = speed
        self.size = size
        self.rect = pygame.Rect((x, y), (self.size))
        self.images = images
        self.frame = 0
        self.image = self.images[self.frame]
        
    def update(self):
        self.frame += 0
        if self.frame >= len(self.images):
            self.frame = 0
        self.image = self.images[self.frame]
        pass

cactus_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
boost_group = pygame.sprite.Group()
boost(random.randrange(0, display_width), 300, (5*boost_images_size[0], 5*boost_images_size[1]), boost_images, 7)
boost.add(boost_group)
cactus(random.randrange(0, display_width), 300, (5*cactus1_images_size[0], 5*cactus2_images_size[1]), cactus2_images, 7)
cactus.add(all_sprites)

class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rockets = 0
        self.boosts = 0
        self.x_change = 0
        self.y_change = 0
        self.w = 128
        self.speed = 0

    def drawCar(self, x, y):
        gameDisplay.blit(wagon_images[0], (x, y))

def movePlayer(object):
    pressed = pygame.key.get_pressed()
    up, down, left, right = [pressed[key] for key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)]
    #up, down, left, right = [pressed[key] for key in (pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)]

    if up:
        object.y_change = -4
    elif down:
        object.y_change = 8
    else:
        object.y_change = 0

    if right:
        object.x_change = 5
    elif left:
        object.x_change = -5
    else:
        object. x_change = 0
    #object.y_change, object.x_change

def generic_text(text, size, color, text_center):
        font = pygame.font.Font("freesansbold.ttf", size)
        rendered_text = font.render(text, True, color)
        gameDisplay.blit(rendered_text, rendered_text.get_rect(center = text_center))
        pygame.display.update()

def crash():
    generic_text("You Crashed", 115, black, (display_width/2, display_height/2))

def button(x, y, w, h, text, text_color, text_size, color, active_color, func = None):
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    but_center = (x+w/2), (y+h/2)

    if x <= mouse_pos[0] <= x+w and y <= mouse_pos[1] <= y+h:
        pygame.draw.rect(gameDisplay, active_color, (x, y, w, h))
        generic_text(text, 20, text_color, but_center)

        if click[0] == 1 and func != None:
            func()
    else:
        pygame.draw.rect(gameDisplay, color, (x, y, w, h))
        generic_text(text, 20, text_color, but_center)

def score(dodged):
    generic_text("Dodged: {}".format(dodged), 30, black, (display_width/10, display_height/10))

def gameIntro():

    intro = True

    while intro:

        gameDisplay.fill(white)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                quit()

        generic_text("Horse Drugs: The Game", 115, black, (display_width/2, display_height/4))

        start_but = button(display_width/2 - 50, display_height/2 - 50, 100, 50, "Start", white, 20, green, bright_green, gameLoop)
        quit_but = button(display_width/2 - 50, display_height/2 + 50, 100, 50, "Quit", white, 20, red, bright_red, quit)

        pygame.display.update()
        clock.tick(60)

def gameLoop():

    # car = Car(display_width*0.45, display_height*0.4)

    dodged = 0

    #obstacles = []
    #obstacles.append(obstacle(random.randrange(0, display_width), -display_height, 24, 40, display_height/60, black))

    display_crash_text = False
    gameExit = False
    #gameDisplay.fill(white)

    while not gameExit:

        

        if pygame.event.peek(pygame.QUIT) == True:
                    pygame.display.quit()
                    pygame.quit()
                    exit()

        # if car.x > display_width-car.w or car.x < 0:
        #     crash_time = time.get_current_time()
        #     crash()

        # for obst in obstacles:
        #     if obst.y > display_height:
        #         obst.y = 0 - random.randrange(0, 300) - obst.h
        #         obst.x = random.randrange(0, display_width-car.w)
        #         dodged += 1
        #         if obst.speed < 20:
        #             obst.speed += 1
                
        #         #if dodged % 10 == 0 and dodged != 0:
        #         obstacles.append(obstacle(random.randrange(0, display_width), -display_height, 24, 40, obst.speed, red))

        #     if not display_crash_text and car.y > obst.y and car.y < obst.y + obst.h and car.x + car.w > obst.x and car.x < obst.x + obst.w:
        #         crash_time = time.time()
        #         display_crash_text = True

        #     if display_crash_text:
        #         obst.speed = 0
        #         crash()
        #         if time.time() - crash_time > 2:
        #             display_crash_text = False
        #             gameLoop()

        #     obst.y += obst.speed
        #     obst.draw()

        # movePlayer(car)
        boost_group.update()
        #cactus_group.update()
        group = boost_group.draw(gameDisplay)
        #cactus_group.draw(gameDisplay)
        # car.x += car.x_change
        # car.y += car.y_change
        # car.drawCar(car.x, car.y)
        # score(dodged)



        fps = int(clock.get_fps())
        #generic_text("FPS: {}".format(fps), 30, black, (display_width/10, display_height/10 + 50))
        print(fps)
        pygame.display.update(boost_group.draw(gameDisplay))
        clock.tick(30)
        

gameLoop()
pygame.display.quit()
pygame.quit()
quit()
