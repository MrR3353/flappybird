import pygame
from random import randint


class PipesCouple():
    def __init__(self, screen):
        self.screen = screen
        # load 2 sprites
        self.images = [pygame.transform.rotate(pygame.image.load('sprites/pipe.png'), 180),
                       pygame.image.load('sprites/pipe.png')]
        w, h = pygame.display.get_surface().get_size()
        self.x = w

        # coords of pipes
        rand = randint(300, 700)
        self.y = [rand - 700, rand]  # [-400; 0] [300; 700]
        self.speed = 2
        self.HEIGHT = 520
        self.WIDTH = 50

    def draw(self):
        self.x -= self.speed
        self.screen.blit(self.images[0], (self.x, self.y[0]))  # showing sprite
        self.screen.blit(self.images[1], (self.x, self.y[1]))