import pygame
import sys
from bird import Bird
from bg import Background
from pipe import PipesCouple
import db

WIDTH, HEIGHT = 864, 750
FPS = 60
pipe_frequency = 3000


def draw_text(text, screen, color, x, y, size=60):
    font = pygame.font.SysFont('Bauhaus 93', size)
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def game_over(screen):
    image = pygame.image.load('sprites/gameover.png')
    image2 = pygame.image.load('sprites/restart.png')
    screen.blit(image, (WIDTH/2 - 96, HEIGHT/2 - 21))
    screen.blit(image2, (WIDTH / 2 - 60, HEIGHT / 2 + 50))
    pygame.display.update()


def get_nickname(screen):
    nickname = ''
    available = True  # is available nickname
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(nickname) > 0 and db.is_available(nickname):
                        return nickname
                    else:
                        available = False
                elif event.key == pygame.K_BACKSPACE:
                    nickname = nickname[:-1]
                    available = True
                elif event.key == pygame.K_SPACE:
                    pass
                else:
                    nickname += event.unicode
                    available = True
        screen.fill((255, 255, 255))
        if not available:
            draw_text("This nickname is TAKEN.", screen, (0, 0, 0), 150, HEIGHT / 2 + 100)
        draw_text("Enter your nickname and press Enter", screen, (0, 0, 0), 50, HEIGHT / 2 - 100)
        draw_text(nickname, screen, (0, 0, 0), WIDTH/2 - len(nickname) * 10, HEIGHT/2)
        pygame.display.update()


def table_score(screen, nickname):
    scores = db.get_all()
    scores.sort(key=lambda a: a[1], reverse=True)
    bg = Background(screen)
    bg.draw()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return
        shift = 0
        draw_text('High scores', screen, (0, 0, 0), WIDTH / 2 - len('High scores') * 10, 20)
        for score in scores:
            draw_text(score[0] + ': ' + str(score[1]), screen, (0, 0, 0), WIDTH / 2 - len(score[0] + ': ' + str(score[1])) * 10, 120 + shift)
            if score[0] == nickname:  # highlight previous score
                draw_text(score[0] + ': ' + str(score[1]), screen, (255, 255, 0),
                          WIDTH / 2 - len(score[0] + ': ' + str(score[1])) * 10, 120 + shift)
            shift += 60
        draw_text("press Enter or Space", screen, (0, 0, 0), 200, 4 * HEIGHT / 6)
        pygame.display.update()


def run():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    nickname = get_nickname(screen)
    clock = pygame.time.Clock()

    score = 0
    bird = Bird(screen)
    bg = Background(screen)
    pipes = [PipesCouple(screen)]
    last_pipe = pygame.time.get_ticks()  # time of creating last pipe

    while True:
        if bird.game_over:
            db.save(nickname, score)
            game_over(screen)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                            table_score(screen, nickname)
                            nickname = get_nickname(screen)
                            score = 0
                            bird = Bird(screen)
                            bg = Background(screen)
                            pipes = [PipesCouple(screen)]
                            last_pipe = pygame.time.get_ticks()  # time of creating last pipe
                if not bird.game_over:
                    break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    bird.jump()
                elif event.key == pygame.K_DOWN:
                    bird.fall()

        bg.draw()

        # deleting useless pipes
        for pipe in pipes:
            pipe.draw()
        if len(pipes) > 3:
            pipes.pop(0)

        # adding new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe = PipesCouple(screen)
            pipes.append(pipe)
            last_pipe = time_now

        bird.draw()
        draw_text(nickname, screen, (0, 0, 0), WIDTH / 2 - len(nickname) * 10, 50)

        # check collisions
        for pipe in pipes:
            if pipe.x - pipe.WIDTH/2 < bird.x < pipe.x + pipe.WIDTH/2:
                if pipe.y[0] + pipe.HEIGHT < bird.y < pipe.y[1]:
                    if bird.x == pipe.x + pipe.WIDTH / 2 - 1:
                        score += 1
                else:
                    bird.game_over = True

        draw_text("Score: " + str(score), screen, (255, 255, 255), 50, 50)
        if score < 1:
            draw_text("Use keyboard arrows or [space] to control bird", screen, (0, 0, 0), 100, 5.5/6 * HEIGHT, size=40)
        pygame.display.update()
        clock.tick(FPS)


run()