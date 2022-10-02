import pygame
import sys
pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
FPS = 20
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
ADD_NEW_BANANA_RATE = 25

vines_img = pygame.image.load('merged_vines_size_1.png')
vines_img_rect = vines_img.get_rect()
vines_img_rect.left = 0
water_img = pygame.image.load('water_border_1.png')
water_img_rect = water_img.get_rect()
water_img_rect.left = 0

CLOCK = pygame.time.Clock()
font = pygame.font.SysFont('forte', 20)

bg = pygame.image.load("bg.png")

canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption('Monkey Mania')


class Monkey:
    monkey_velocity = 10

    def __init__(self):
        self.monkey = pygame.image.load('monkey_size_1.png')
        self.monkey_img = pygame.transform.scale(self.monkey, (100, 100))
        self.monkey_img_rect = self.monkey_img.get_rect()
        self.monkey_img_rect.width -= 10
        self.monkey_img_rect.height -= 10
        self.monkey_img_rect.top = SCREEN_HEIGHT/2
        self.monkey_img_rect.right = SCREEN_WIDTH
        self.up = True
        self.down = False

    def update(self):
        canvas.blit(self.monkey_img, self.monkey_img_rect)
        if self.monkey_img_rect.top <= vines_img_rect.bottom:
            self.up = False
            self.down = True
        elif self.monkey_img_rect.bottom >= water_img_rect.top:
            self.up = True
            self.down = False

        if self.up:
            self.monkey_img_rect.top -= self.monkey_velocity
        elif self.down:
            self.monkey_img_rect.top += self.monkey_velocity


class Bananas:
    bananas_velocity = 20

    def __init__(self):
        self.bananas = pygame.image.load('Bananas.png')
        self.bananas_img = pygame.transform.scale(self.bananas, (50, 50))
        self.bananas_img_rect = self.bananas_img.get_rect()
        self.bananas_img_rect.right = monkey.monkey_img_rect.left
        self.bananas_img_rect.top = monkey.monkey_img_rect.top + 30


    def update(self):
        canvas.blit(self.bananas_img, self.bananas_img_rect)

        if self.bananas_img_rect.left > 0:
            self.bananas_img_rect.left -= self.bananas_velocity


class Character:
    velocity = 10

    def __init__(self):
        self.character_img = pygame.image.load('character.png')
        self.character_img_rect = self.character_img.get_rect()
        self.character_img_rect.left = 20
        self.character_img_rect.top = SCREEN_HEIGHT/2 - 100
        self.down = True
        self.up = False

    def update(self):
        canvas.blit(self.character_img, self.character_img_rect)
        if self.character_img_rect.top <= vines_img_rect.bottom:
            game_over()
            if SCORE > self.character_score:
                self.character_score = SCORE
        if self.character_img_rect.bottom >= water_img_rect.top:
            game_over()
            if SCORE > self.character_score:
                self.character_score = SCORE
        if self.up:
            self.character_img_rect.top -= 10
        if self.down:
            self.character_img_rect.bottom += 10


def game_over():
    game_over_img = pygame.image.load('gameover.png')
    game_over_img_rect = game_over_img.get_rect()
    game_over_img_rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    canvas.blit(game_over_img, game_over_img_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                game_loop()
        pygame.display.update()


def start_game():
    #canvas.fill(WHITE)
    canvas.blit(bg, [0,0])
    start_img = pygame.image.load('start.png')
    start_img_rect = start_img.get_rect()
    start_img_rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    canvas.blit(start_img, start_img_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                game_loop()
        pygame.display.update()    


def game_loop():
    while True:
        global monkey
        monkey = Monkey()
        bananas = Bananas()
        character = Character()
        add_new_banana_counter = 0
        global SCORE
        SCORE = 0
        global  HIGH_SCORE
        bananas_list = []
        while True:
            canvas.blit(bg, [0,0])
            vines_img_rect.bottom = 50
            water_img_rect.top = SCREEN_HEIGHT - 50
            monkey.update()
            add_new_banana_counter += 1

            if add_new_banana_counter == ADD_NEW_BANANA_RATE:
                add_new_banana_counter = 0
                new_banana = Bananas()
                bananas_list.append(new_banana)
            for f in bananas_list:
                if f.bananas_img_rect.left <= 0:
                    bananas_list.remove(f)
                    SCORE += 1
                f.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        character.up = True
                        character.down = False
                    elif event.key == pygame.K_DOWN:
                        character.down = True
                        character.up = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        character.up = False
                        character.down = True
                    elif event.key == pygame.K_DOWN:
                        character.down = True
                        character.up = False

            score_font = font.render('Score:'+str(SCORE), True, WHITE)
            score_font_rect = score_font.get_rect()
            score_font_rect.center = (1100, vines_img_rect.bottom + score_font_rect.height/2)
            canvas.blit(score_font, score_font_rect)

            canvas.blit(vines_img, vines_img_rect)
            canvas.blit(water_img, water_img_rect)
            character.update()
            for f in bananas_list:
                if f.bananas_img_rect.colliderect(character.character_img_rect):
                    game_over()
                    if SCORE > character.character_score:
                        character.character_score = SCORE
            pygame.display.update()
            CLOCK.tick(FPS)

start_game()