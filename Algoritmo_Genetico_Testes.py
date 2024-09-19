import os
import sys
import pygame
import random
import numpy as np
from pygame import *

pygame.mixer.pre_init(44100, -16, 2, 2048)  # fix audio delay
pygame.init()

scr_size = (width, height) = (600, 150)
FPS = 60
gravity = 0.6

black = (0, 0, 0)
white = (255, 255, 255)
background_col = (235, 235, 235)

high_score = 0

screen = pygame.display.set_mode(scr_size)
clock = pygame.time.Clock()
pygame.display.set_caption("T-Rex Rush")

jump_sound = pygame.mixer.Sound('sprites/jump.wav')
die_sound = pygame.mixer.Sound('sprites/die.wav')
checkPoint_sound = pygame.mixer.Sound('sprites/checkPoint.wav')


def load_image(name, sizex=-1, sizey=-1, colorkey=None):
    fullname = os.path.join('sprites', name)
    image = pygame.image.load(fullname)
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)

    if sizex != -1 or sizey != -1:
        image = pygame.transform.scale(image, (sizex, sizey))

    return image, image.get_rect()


def load_sprite_sheet(sheetname, nx, ny, scalex=-1, scaley=-1, colorkey=None):
    fullname = os.path.join('sprites', sheetname)
    sheet = pygame.image.load(fullname)
    sheet = sheet.convert()

    sheet_rect = sheet.get_rect()
    sprites = []

    sizex = sheet_rect.width / nx
    sizey = sheet_rect.height / ny

    for i in range(0, ny):
        for j in range(0, nx):
            rect = pygame.Rect((j * sizex, i * sizey, sizex, sizey))
            image = pygame.Surface(rect.size)
            image = image.convert()
            image.blit(sheet, (0, 0), rect)

            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey, RLEACCEL)

            if scalex != -1 or scaley != -1:
                image = pygame.transform.scale(image, (scalex, scaley))

            sprites.append(image)

    sprite_rect = sprites[0].get_rect()

    return sprites, sprite_rect


class Scoreboard():
    def __init__(self, x=-1, y=-1):
        self.score = 0
        self.tempimages, self.temprect = load_sprite_sheet('numbers.png', 12, 1, 11, int(11 * 6 / 5), -1)
        self.image = pygame.Surface((55, int(11 * 6 / 5)))
        self.rect = self.image.get_rect()
        self.font = pygame.font.Font(None, 20)  # Fonte para a palavra "Score"
        if x == -1:
            self.rect.left = width * 0.89
        else:
            self.rect.left = x
        if y == -1:
            self.rect.top = height * 0.1
        else:
            self.rect.top = y

    def draw(self):
        score_text = self.font.render('Score', True, black)  # Renderizar "Score"
        screen.blit(score_text, (self.rect.left - 100, self.rect.top))  # Desenhar "Score"
        screen.blit(self.image, self.rect)

    def update(self, score):
        score_digits = self.extract_digits(score)
        self.image.fill(background_col)
        for s in score_digits:
            self.image.blit(self.tempimages[s], self.temprect)
            self.temprect.left += self.temprect.width
        self.temprect.left = 0

    def extract_digits(self, number):
        if number > -1:
            digits = []
            while number / 10 != 0:
                digits.append(number % 10)
                number = int(number / 10)

            digits.append(number % 10)
            while len(digits) < 5:
                digits.append(0)
            digits.reverse()
            return digits


class Dino():
    def __init__(self, sizex=-1, sizey=-1):
        self.images, self.rect = load_sprite_sheet('dino.png', 5, 1, sizex, sizey, -1)
        self.images1, self.rect1 = load_sprite_sheet('dino_ducking.png', 2, 1, 59, sizey, -1)
        self.rect.bottom = int(0.98 * height)
        self.rect.left = width / 15
        self.image = self.images[0]
        self.index = 0
        self.counter = 0
        self.score = 0
        self.isJumping = False
        self.isDead = False
        self.isDucking = False
        self.movement = [0, 0]
        self.jumpSpeed = 11.5
        self.ground_height = int(0.98 * height)  # Altura do chão para verificação

    def draw(self):
        screen.blit(self.image, self.rect)

    def checkbounds(self):
        if self.rect.bottom >= self.ground_height:  # Garantir que ele não pule mais uma vez até estar no chão
            self.rect.bottom = self.ground_height
            self.isJumping = False  # Ele só pode pular novamente quando tocar o chão

    def jump(self):
        if not self.isJumping:  # Verificar se já está pulando
            self.isJumping = True
            self.movement[1] = -1 * self.jumpSpeed
            jump_sound.play()

    def duck(self, ducking):
        self.isDucking = ducking

    def update(self):
        if self.isJumping:
            self.movement[1] += gravity

        if self.isJumping:
            self.index = 0
        elif self.isDucking:
            if self.counter % 5 == 0:
                self.index = (self.index + 1) % 2
        else:
            if self.counter % 5 == 0:
                self.index = (self.index + 1) % 2 + 2

        if self.isDead:
            self.index = 4

        if not self.isDucking:
            self.image = self.images[self.index]
        else:
            self.image = self.images1[self.index % 2]

        self.rect = self.rect.move(self.movement)
        self.checkbounds()

        if not self.isJumping and not self.isDead:
            self.score += 2  # Aumenta mais a pontuação enquanto está no chão
        elif not self.isDead:
            self.score += 1  # Menos pontos quando está no ar


class Cactus(pygame.sprite.Sprite):
    def __init__(self, speed=5, sizex=-1, sizey=-1):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images, self.rect = load_sprite_sheet('cacti-small.png', 3, 1, sizex, sizey, -1)
        self.rect.bottom = int(0.98 * height)
        self.rect.left = width + self.rect.width
        self.image = self.images[random.randrange(0, 3)]
        self.movement = [-1 * speed, 0]

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)
        if self.rect.right < 0:
            self.kill()


class Ptera(pygame.sprite.Sprite):
    def __init__(self, speed=5, sizex=-1, sizey=-1):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images, self.rect = load_sprite_sheet('ptera.png', 2, 1, sizex, sizey, -1)
        self.ptera_height = [height * 0.82, height * 0.75, height * 0.60]
        self.rect.centery = self.ptera_height[random.randrange(0, 3)]
        self.rect.left = width + self.rect.width
        self.image = self.images[0]
        self.movement = [-1 * speed, 0]
        self.index = 0
        self.counter = 0

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        if self.counter % 10 == 0:
            self.index = (self.index + 1) % 2
        self.image = self.images[self.index]
        self.rect = self.rect.move(self.movement)
        self.counter += 1
        if self.rect.right < 0:
            self.kill()


class Ground():
    def __init__(self, speed=-5):
        self.image, self.rect = load_image('ground.png', -1, -1, -1)
        self.image1, self.rect1 = load_image('ground.png', -1, -1, -1)
        self.rect.bottom = height
        self.rect1.bottom = height
        self.rect1.left = self.rect.right
        self.speed = speed

    def draw(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.image1, self.rect1)

    def update(self):
        self.rect.left += self.speed
        self.rect1.left += self.speed

        if self.rect.right < 0:
            self.rect.left = self.rect1.right

        if self.rect1.right < 0:
            self.rect1.left = self.rect.right


class Population:
    def __init__(self, size, mutation_rate=0.1):
        self.size = size
        self.mutation_rate = mutation_rate
        self.dinosaurs = [self.create_dino() for _ in range(size)]
        self.scores = np.zeros(size)

    def create_dino(self):
        return Dino(44, 47)

    def evaluate(self):
        for i, dino in enumerate(self.dinosaurs):
            if not dino.isDead:
                self.scores[i] = dino.score
        return self.scores

    def select(self):
        total_fitness = np.sum(self.scores)
        
        def select(self):
            total_fitness = np.sum(self.scores)
    
        # Verifique se o total_fitness é zero
        if total_fitness == 0:
        # Seleciona dois pais aleatoriamente se o fitness total for zero
            parents_idx = np.random.choice(range(self.size), size=2)
        else:
            selection_probs = self.scores / total_fitness
            parents_idx = np.random.choice(range(self.size), size=2, p=selection_probs)

        return self.dinosaurs[parents_idx[0]], self.dinosaurs[parents_idx[1]]

    def cross_over(self, parent1, parent2):
        child = self.create_dino()
        child.jumpSpeed = (parent1.jumpSpeed + parent2.jumpSpeed) / 2
        return child

    def mutate(self, dino):
        if random.random() < self.mutation_rate:
            dino.jumpSpeed += random.uniform(-1, 1)
        return dino

    def evolve(self):
        new_generation = []
        for _ in range(self.size):
            parent1, parent2 = self.select()
            child = self.cross_over(parent1, parent2)
            child = self.mutate(child)
            new_generation.append(child)
        self.dinosaurs = new_generation


def gameplay():
    global high_score
    gamespeed = 4
    gameOver = False
    gameQuit = False
    population = Population(size=10)
    new_ground = Ground(-1 * gamespeed)
    scoreboard = Scoreboard()

    cacti = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()

    Cactus.containers = cacti
    Ptera.containers = pteras

    counter = 0

    while not gameQuit:
        while not gameOver:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameQuit = True
                    gameOver = True

            for dino in population.dinosaurs:
                if not dino.isDead:
                    # Lógica para pular ao encontrar um cacto
                    for c in cacti:
                        distance_to_cactus = c.rect.left - dino.rect.right
                        if 10 < distance_to_cactus < 30 and not dino.isJumping:  # Pular apenas se não estiver no ar e detectar um cacto à frente
                            dino.jump()

                    # Lógica para abaixar ao encontrar um pterossauro em uma altura baixa
                    for p in pteras:
                        if p.rect.left < dino.rect.right + 50 and p.rect.centery > height * 0.75:
                            dino.duck(True)
                        else:
                            dino.duck(False)

            # Gerar novos cactos e pterossauros
            if len(cacti) < 2:
                if len(cacti) == 0:
                    last_obstacle.empty()
                    last_obstacle.add(Cactus(gamespeed, 40, 40))
                else:
                    for l in last_obstacle:
                        if l.rect.right < width * 0.7 and random.randrange(0, 50) == 10:
                            last_obstacle.empty()
                            last_obstacle.add(Cactus(gamespeed, 40, 40))

            # Adicionar pterossauro a cada 500 pontos
            for dino in population.dinosaurs:
                if dino.score % 500 == 0 and len(pteras) == 0:
                    last_obstacle.empty()
                    last_obstacle.add(Ptera(gamespeed, 46, 40))

            pteras.update()  # Atualizar pterossauros

            for dino in population.dinosaurs:
                dino.update()
                scoreboard.update(dino.score)

                for c in cacti:
                    c.movement[0] = -1 * gamespeed
                    if pygame.sprite.collide_mask(dino, c):
                        dino.isDead = True
                        die_sound.play()

                for p in pteras:
                    p.movement[0] = -1 * gamespeed
                    if pygame.sprite.collide_mask(dino, p):
                        dino.isDead = True
                        die_sound.play()

            if all([dino.isDead for dino in population.dinosaurs]):
                population.evaluate()
                population.evolve()
                gameOver = True

            new_ground.update()
            cacti.update()
            pteras.update()

            screen.fill(background_col)
            new_ground.draw()
            cacti.draw(screen)
            pteras.draw(screen)
            scoreboard.draw()  # Desenhar o placar
            for dino in population.dinosaurs:
                dino.draw()
            pygame.display.update()
            clock.tick(FPS)

    pygame.quit()



def main():
    gameplay()


main()