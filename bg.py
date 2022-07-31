import pygame


class Background():
    def __init__(self, screen):
        self.screen = screen
        self.image = pygame.image.load('sprites/bg.png')
        self.scroll = 0
        self.scroll_speed = 3

    def draw(self):
        self.screen.blit(self.image, (self.scroll, 0))
        self.screen.blit(self.image, (self.scroll + 431, 0))
        self.scroll -= self.scroll_speed
        if self.scroll < -431:
            self.scroll = 0

