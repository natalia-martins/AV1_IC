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

# Funções de carregamento de imagem
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

    return (image, image.get_rect())

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

# Classe Dino com lógica de movimento e controle
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
        self.isBlinking = False
        self.movement = [0, 0]
        self.jumpSpeed = 11.5

        self.stand_pos_width = self.rect.width
        self.duck_pos_width = self.rect1.width

    def draw(self):
        screen.blit(self.image, self.rect)

    def checkbounds(self):
        if self.rect.bottom > int(0.98 * height):
            self.rect.bottom = int(0.98 * height)
            self.isJumping = False

    def update(self):
        if self.isJumping:
            self.movement[1] = self.movement[1] + gravity

        if self.isJumping:
            self.index = 0
        elif self.isBlinking:
            if self.index == 0:
                if self.counter % 400 == 399:
                    self.index = (self.index + 1) % 2
            else:
                if self.counter % 20 == 19:
                    self.index = (self.index + 1) % 2

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
            self.rect.width = self.stand_pos_width
        else:
            self.image = self.images1[(self.index) % 2]
            self.rect.width = self.duck_pos_width

        self.rect = self.rect.move(self.movement)
        self.checkbounds()

        if not self.isDead and self.counter % 7 == 6 and self.isBlinking == False:
            self.score += 1
            if self.score % 100 == 0 and self.score != 0:
                if pygame.mixer.get_init() != None:
                    checkPoint_sound.play()

        self.counter = (self.counter + 1)

# Classes de obstáculos
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
        self.counter = (self.counter + 1)
        if self.rect.right < 0:
            self.kill()

# Implementação do algoritmo evolutivo
class DinoAgent:
    def __init__(self):
        # Rede neural simples com pesos aleatórios
        self.weights = np.random.randn(4)  # Exemplo de 4 pesos

    def decide(self, inputs):
        result = np.dot(self.weights, inputs)
        if result > 0.5:
            return 'jump'
        elif result < -0.5:
            return 'duck'
        else:
            return 'run'

def evaluate_agent(agent):
    playerDino = Dino(44, 47)
    score = 0
    gameOver = False
    gamespeed = 4

    # Inicialização dos grupos de obstáculos
    cacti = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()

    Cactus.containers = cacti
    Ptera.containers = pteras

    while not gameOver:
        obstacle = None
        if len(cacti) > 0:
            obstacle = cacti.sprites()[0]
        elif len(pteras) > 0:
            obstacle = pteras.sprites()[0]

        # Lógica de decisão do agente: só age se um obstáculo estiver perto
        if obstacle:
            state = [obstacle.rect.left, obstacle.rect.bottom, gamespeed, playerDino.rect.bottom]

            # Aumentamos a distância para o pulo ocorrer com antecedência suficiente
            if isinstance(obstacle, Cactus) and obstacle.rect.left < 250:
                action = agent.decide(state)
                # Certifique-se de que o dinossauro está no chão antes de pular
                if action == 'jump' and playerDino.rect.bottom == int(0.98 * height):
                    playerDino.isJumping = True
                    playerDino.movement[1] = -1 * playerDino.jumpSpeed

            # Só abaixa se o obstáculo for um pterossauro e estiver voando baixo
            elif isinstance(obstacle, Ptera) and obstacle.rect.left < 250 and obstacle.rect.centery > playerDino.rect.bottom - 30:
                action = agent.decide(state)
                if action == 'duck':
                    playerDino.isDucking = True
            else:
                playerDino.isDucking = False

        # Atualizar o dinossauro e os obstáculos
        playerDino.update()
        cacti.update()
        pteras.update()

        # Renderização do jogo durante a avaliação do agente
        screen.fill(background_col)
        playerDino.draw()
        cacti.draw(screen)
        pteras.draw(screen)
        pygame.display.update()
        clock.tick(FPS)

        # Checar colisões
        for c in cacti:
            if pygame.sprite.collide_mask(playerDino, c):
                playerDino.isDead = True
        for p in pteras:
            if pygame.sprite.collide_mask(playerDino, p):
                playerDino.isDead = True

        # Terminar o jogo se o dinossauro morrer
        if playerDino.isDead:
            gameOver = True
        else:
            score += 1

        # Adicionar novos obstáculos
        if len(cacti) < 2:
            if len(cacti) == 0:
                last_obstacle.empty()
                last_obstacle.add(Cactus(gamespeed, 40, 40))
            else:
                for l in last_obstacle:
                    if l.rect.right < width * 0.7 and random.randrange(0, 50) == 10:
                        last_obstacle.empty()
                        last_obstacle.add(Cactus(gamespeed, 40, 40))

        if len(pteras) == 0 and random.randrange(0, 200) == 10 and score > 500:
            for l in last_obstacle:
                if l.rect.right < width * 0.8:
                    last_obstacle.empty()
                    last_obstacle.add(Ptera(gamespeed, 46, 40))

    return score



def select(population, fitness_scores):
    selected = np.random.choice(population, size=2, p=fitness_scores/np.sum(fitness_scores))
    return selected[0], selected[1]

def crossover(parent1, parent2):
    cut_point = np.random.randint(0, len(parent1.weights))
    child1_weights = np.concatenate((parent1.weights[:cut_point], parent2.weights[cut_point:]))
    child2_weights = np.concatenate((parent2.weights[:cut_point], parent1.weights[cut_point:]))
    child1 = DinoAgent()
    child2 = DinoAgent()
    child1.weights = child1_weights
    child2.weights = child2_weights
    return child1, child2

def mutate(agent, mutation_rate=0.1):
    for i in range(len(agent.weights)):
        if np.random.rand() < mutation_rate:
            agent.weights[i] += np.random.randn()
    return agent

def genetic_algorithm():
    population_size = 20
    generations = 50
    mutation_rate = 0.1
    population = [DinoAgent() for _ in range(population_size)]

    for generation in range(generations):
        fitness_scores = np.array([evaluate_agent(agent) for agent in population])
        print(f"Geração {generation}: Melhor pontuação = {np.max(fitness_scores)}")

        new_population = []
        for _ in range(population_size // 2):
            parent1, parent2 = select(population, fitness_scores)
            child1, child2 = crossover(parent1, parent2)
            new_population.extend([mutate(child1, mutation_rate), mutate(child2, mutation_rate)])
        
        population = new_population

    best_agent = population[np.argmax(fitness_scores)]
    return best_agent

# Função de tela de introdução
# Importações e outras definições de classes, como Dino, Cactus, etc...

# Função de tela de introdução
def introscreen():
    # Implementação da tela de introdução
    temp_dino = Dino(44, 47)
    temp_dino.isBlinking = True
    gameStart = False

    temp_ground, temp_ground_rect = load_sprite_sheet('ground.png', 15, 1, -1, -1, -1)
    temp_ground_rect.left = width / 20
    temp_ground_rect.bottom = height

    logo, logo_rect = load_image('logo.png', 240, 40, -1)
    logo_rect.centerx = width * 0.6
    logo_rect.centery = height * 0.6

    while not gameStart:
        if pygame.display.get_surface() == None:
            print("Nao foi possivel carregar a superficie de exibicao")
            return True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        temp_dino.isJumping = True
                        temp_dino.isBlinking = False
                        temp_dino.movement[1] = -1 * temp_dino.jumpSpeed

        temp_dino.update()

        if pygame.display.get_surface() != None:
            screen.fill(background_col)
            screen.blit(temp_ground[0], temp_ground_rect)
            if temp_dino.isBlinking:
                screen.blit(logo, logo_rect)
            temp_dino.draw()

            pygame.display.update()

        clock.tick(FPS)
        if temp_dino.isJumping == False and temp_dino.isBlinking == False:
            gameStart = True

    return False

# Função principal de gameplay
def gameplay(agent=None):
    # Insira aqui a função gameplay completa que forneci anteriormente
    # Toda a lógica de jogo, controle do dinossauro, obstáculos, e colisões.
    pass

# Função principal
def main():
    isGameQuit = introscreen()  # Chama a tela de introdução
    if not isGameQuit:
        best_dino = genetic_algorithm()  # Executa o algoritmo genético para treinar o dinossauro
        gameplay(best_dino)  # Inicia o jogo com o melhor dinossauro

# Execução do jogo
main()

