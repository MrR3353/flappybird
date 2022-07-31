import pygame


class Bird():
    def __init__(self, screen):
        self.screen = screen
        self.frame = 0
        self.frame_speed = 0.1
        self.images = [pygame.image.load('sprites/yellowbird-1.png'),
                       pygame.image.load('sprites/yellowbird-2.png'),
                       pygame.image.load('sprites/yellowbird-3.png')]
        self.image = self.images[int(self.frame)]
        w, h = pygame.display.get_surface().get_size()
        self.x = w / 3
        self.y = h / 2
        self.speed = 0
        self.game_over = False

    def draw(self):
        self.speed += 0.4   # speed for y axis
        self.y += int(self.speed)

        if self.y > 700:    # game over
            self.game_over = True

        self.image = pygame.transform.rotate(self.images[int(self.frame)], self.speed * -2)  # rotate bird in fly

        if self.game_over:
            self.image = pygame.transform.rotate(self.images[int(self.frame)], -90)

        self.screen.blit(self.image, (self.x, self.y))  # showing sprite
        self.frame += self.frame_speed  # frame changing
        if int(self.frame) == 3:
            self.frame = 0

    def jump(self):
        self.speed = -10

    def fall(self):
        self.speed = 5
