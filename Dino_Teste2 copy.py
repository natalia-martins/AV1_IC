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

# Função auxiliar para carregar imagem
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

# Função auxiliar para carregar spritesheets
def load_sprite_sheet(sheetname, nx, ny, scalex=-1, scaley=-1, colorkey=None):
    fullname = os.path.join('sprites', sheetname)
    sheet = pygame.image.load(fullname)
    sheet = sheet.convert()

    sheet_rect = sheet.get_rect()
    sprites = []
    sizex = sheet_rect.width / nx
    sizey = sheet_rect.height / ny

    for i in range(ny):
        for j in range(nx):
            rect = pygame.Rect((j * sizex, i * sizey, sizex, sizey))
            image = pygame.Surface(rect.size)
            image = image.convert()
            image.blit(sheet, (0, 0), rect)

            if colorkey is not None:
                if colorkey == -1:
                    colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey, RLEACCEL)

            # Apenas escala se os valores scalex e scaley forem válidos
            if scalex > 0 and scaley > 0:
                image = pygame.transform.scale(image, (scalex, scaley))

            sprites.append(image)

    sprite_rect = sprites[0].get_rect()
    return sprites, sprite_rect

def extractDigits(number):
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

class Scoreboard():
    def __init__(self, x=-1, y=-1):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)  # Definir o estilo da fonte
        self.score = 0
        self.tempimages, self.temprect = load_sprite_sheet('numbers.png', 12, 1, 11, int(11 * 6 / 5), -1)
        self.image = pygame.Surface((55, int(11 * 6 / 5)))
        self.rect = self.image.get_rect()
        if x == -1:
            self.rect.left = width * 0.89
        else:
            self.rect.left = x
        if y == -1:
            self.rect.top = height * 0.1
        else:
            self.rect.top = y

    def display_score(self, score, position):
        score_text = self.font.render(f'Score: {score}', True, (255, 255, 255))  # Cor branca
        self.screen.blit(score_text, position)  # Desenhar o texto na tela na posição fornecida

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self, score):
        score_digits = extractDigits(score)
        self.image.fill(background_col)
        for s in score_digits:
            self.image.blit(self.tempimages[s], self.temprect)
            self.temprect.left += self.temprect.width
        self.temprect.left = 0

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

class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image, self.rect = load_image('cloud.png', int(90 * 30 / 42), 30, -1)
        self.rect.left = x
        self.rect.top = y
        self.movement = [-1, 0]  # Movimento da nuvem para a esquerda

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)
        if self.rect.right < 0:
            self.kill()  # Remove a nuvem se ela sair da tela

# Classe Dino original
class Dino():
    def __init__(self, sizex=-1, sizey=-1):
        pygame.sprite.Sprite.__init__(self)
        self.images, self.rect = load_sprite_sheet('dino.png', 5, 1, 44, 47, -1) # Imagens normais do dino
        self.images1, self.rect1 = load_sprite_sheet('dino_ducking.png', 2, 1, 59, 30, -1) # Imagens do dino abaixado
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

    def duck(self):
        self.isDucking = True
        self.rect = self.duck_rect  # Ajusta o tamanho da caixa de colisão

    def stand_up(self):
        self.isDucking = False
        self.rect = self.rect.inflate(self.stand_pos_width, self.rect.height)

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

# Classe DinoGA para os dinossauros com algoritmo genético
class DinoGA(Dino):
    def __init__(self, sizex=-1, sizey=-1, color=None):
        super().__init__(sizex, sizey)
        self.color = color
        self.weights = np.random.randn(2)  # Pesos aleatórios iniciais para controle
        self.is_best = False  # Para distinguir o melhor dinossauro
        self.score = 0 # Inicializa a pontuação do dinossauro

    def mutate(self, mutation_rate=0.01):
        """Mutação simples, alterando os pesos"""
        for i in range(len(self.weights)):
            if random.random() < mutation_rate:
                self.weights[i] += np.random.randn()

    def crossover(self, other):
        """Crossover simples entre dois dinossauros"""
        child = DinoGA()
        crossover_point = random.randint(0, len(self.weights) - 1)
        child.weights[:crossover_point] = self.weights[:crossover_point]
        child.weights[crossover_point:] = other.weights[crossover_point:]
        return child

    def decide_jump(self, obstacle_distance):
        """Decide se o dinossauro deve pular com base nos pesos e na distância do obstáculo"""
        # Garantir que só pule quando realmente necessário
        weighted_sum = self.weights[0] * obstacle_distance + self.weights[1]
        
        # Limite o pulo para quando a distância for significativa e evite pulos incontroláveis
        if obstacle_distance > 0 and weighted_sum > 1.5:  # Ajuste o limite aqui
            return True
        return False

    def draw(self):
        if self.is_best:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)  # O melhor dinossauro tem borda vermelha
        else:
            screen.blit(self.image, self.rect)
    
    def update(self):
        if self.isJumping:
            self.movement[1] += gravity

        if self.isJumping:
            self.index = 0
        else:
            if self.isDucking:
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
            self.image = self.images1[(self.index) % 2]

        self.rect = self.rect.move(self.movement)
        self.checkbounds()

        # Atualizar a pontuação com base no tempo sobrevivido
        if not self.isDead and self.counter % 7 == 6:
            self.score += 1
            if self.score % 100 == 0 and self.score != 0:
                if pygame.mixer.get_init() != None:
                    checkPoint_sound.play()

        self.counter = (self.counter + 1)

# Classe GeneticAlgorithm para controlar a população
class GeneticAlgorithm:
    def __init__(self, population_size=3, mutation_rate=0.01, generations=50):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.population = [DinoGA(color=color) for color in [(0, 255, 0), (0, 0, 255), (255, 255, 0)]]  # Dinossauros de cores diferentes
        self.best_agent = None

    def select_parents(self):
        """Seleciona dois dinossauros com base no fitness (pontuação)"""
        fitness_scores = [dino.score for dino in self.population]
        total_fitness = sum(fitness_scores)
        if total_fitness == 0:
            return random.sample(self.population, 2)
        selection_probs = [score / total_fitness for score in fitness_scores]
        parents = np.random.choice(self.population, size=2, p=selection_probs)
        return parents

    def evolve(self):
        """Evolui a população aplicando seleção, crossover e mutação"""
        new_population = []
        self.population = sorted(self.population, key=lambda x: x.score, reverse=True)
        self.best_agent = self.population[0]  # O melhor dinossauro da geração atual
        self.best_agent.is_best = True

        # Manter o melhor indivíduo
        new_population.append(self.best_agent)

        while len(new_population) < self.population_size:
            parent1, parent2 = self.select_parents()
            child = parent1.crossover(parent2)
            child.mutate(self.mutation_rate)
            new_population.append(child)

        self.population = new_population

    def save_best_weights(self):
        """Salva os pesos do melhor dinossauro"""
        best_weights = self.best_agent.weights
        with open('best_dino_weights.json', 'w') as f:
            json.dump(best_weights.tolist(), f)

# Função de gameplay para executar o algoritmo genético
def gameplay_ga(ga):
    global high_score
    gamespeed = 4
    gameOver = False
    gameQuit = False
    new_ground = Ground(-1 * gamespeed)
    scb = Scoreboard()
    highsc = Scoreboard(width * 0.78)
    counter = 0

    cacti = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()

    Cactus.containers = cacti
    Ptera.containers = pteras
    Cloud.containers = clouds

    dino_player = Dino()  # Dino controlado pelo jogador
    dino_ga = DinoGA(color=(0, 255, 0))  # Dino controlado pelo algoritmo genético

    obstacle_timer = 0  # Controla o tempo entre a criação de obstáculos

    player_score = 0
    ga_score = 0

    while not gameQuit:
        while not gameOver:
            if pygame.display.get_surface() == None:
                gameQuit = True
                gameOver = True
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = True
                    # Controles do dino tradicional
                    if event.type == KEYDOWN:
                        if event.key == K_SPACE and not dino_player.isJumping:
                            dino_player.isJumping = True
                            if pygame.mixer.get_init() != None:
                                jump_sound.play()
                            dino_player.movement[1] = -1 * dino_player.jumpSpeed
                        if event.key == K_DOWN and not dino_player.isJumping:  # Se abaixar
                            dino_player.duck()

                    if event.type == KEYUP:
                        if event.key == K_DOWN:  # Levantar quando soltar a tecla
                            dino_player.stand_up()

            # Atualizar dino tradicional
            dino_player.update()

            # Atualiza o estado do dino controlado pelo algoritmo genético
            obstacle_distance = min([c.rect.left - dino_ga.rect.right for c in cacti] or [float('inf')])
            if not dino_ga.isJumping and dino_ga.decide_jump(obstacle_distance):
                dino_ga.isJumping = True
                if pygame.mixer.get_init() != None:
                    jump_sound.play()
                dino_ga.movement[1] = -1 * dino_ga.jumpSpeed

            dino_ga.update()

            # Atualizando a pontuação do jogador e do algoritmo
            player_score += 1
            ga_score += 1

            # Resto da lógica de obstáculos e desenho continua a mesma
            # Atualizar os obstáculos
            for c in cacti:
                c.movement[0] = -1 * gamespeed
                if pygame.sprite.collide_mask(dino_player, c):
                    dino_player.isDead = True
                    if pygame.mixer.get_init() != None:
                        die_sound.play()
                if pygame.sprite.collide_mask(dino_ga, c):
                    dino_ga.isDead = True
                    if pygame.mixer.get_init() != None:
                        die_sound.play()

            for p in pteras:
                p.movement[0] = -1 * gamespeed
                if pygame.sprite.collide_mask(dino_player, p):
                    dino_player.isDead = True
                    if pygame.mixer.get_init() != None:
                        die_sound.play()
                if pygame.sprite.collide_mask(dino_ga, p):
                    dino_ga.isDead = True
                    if pygame.mixer.get_init() != None:
                        die_sound.play()

            # Geração de obstáculos
            obstacle_timer += 1
            if obstacle_timer > random.randint(150, 300):
                if random.random() < 0.7:
                    Cactus(gamespeed)
                else:
                    Ptera(gamespeed)
                obstacle_timer = 0

            # Atualizações de sprites e tela
            cacti.update()
            pteras.update()
            clouds.update()

            screen.fill(background_col)
            new_ground.draw()
            clouds.draw(screen)

            scb.draw()

            # Exibir a pontuação do jogador e do dino do algoritmo genético
            scb.display_score(player_score, (10, 10))  # Posição no canto superior esquerdo para o jogador
            scb.display_score(ga_score, (width - 150, 10))  # Posição no canto superior direito para o GA

            highsc.update(high_score)
            if high_score != 0:
                highsc.draw()
            cacti.draw(screen)
            pteras.draw(screen)

            # Desenhar os dinossauros
            dino_player.draw()
            dino_ga.draw()

            pygame.display.update()
            clock.tick(FPS)

            # Verifica se o jogo terminou
            if dino_player.isDead and dino_ga.isDead:
                gameOver = True
                high_score = max(dino_player.score, dino_ga.score)

                # Exibir a mensagem de quem venceu
                if player_score > ga_score:
                    display_winner("Você venceu!", screen)
                elif ga_score > player_score:
                    display_winner("Algoritmo Genético venceu!", screen)
                else:
                    display_winner("Empate!", screen)

            if counter % 700 == 699:
                new_ground.speed -= 1
                gamespeed += 1

            counter += 1

    pygame.quit()

def display_winner(message, screen):
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, (0, 255, 0))  # Verde para a mensagem
    text_rect = text.get_rect(center=(width / 2, height / 2))  # Centraliza o texto na tela
    screen.blit(text, text_rect)  # Desenha o texto na tela
    pygame.display.update()  # Atualiza a tela para exibir o texto
    pygame.time.delay(2000)  # Pausa por 2 segundos para que a mensagem possa ser lida

    
# Função principal para executar o jogo com algoritmo genético
def main_ga():
    ga = GeneticAlgorithm()
    gameplay_ga(ga)
    ga.save_best_weights()

if __name__ == "__main__":
    main_ga()
