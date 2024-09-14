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


# Dinossauro com Algoritmo Genético
class DinoGA(Dino):
    def __init__(self, sizex=-1, sizey=-1, color=None):
        super().__init__(sizex, sizey)
        self.color = color
        self.weights = np.random.randn(2)  # Pesos aleatórios iniciais para controle
        self.is_best = False  # Para distinguir o melhor dinossauro

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
        weighted_sum = self.weights[0] * obstacle_distance + self.weights[1]
        return weighted_sum > 0

    def draw(self):
        if self.is_best:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)  # O melhor dinossauro tem borda vermelha
        else:
            screen.blit(self.image, self.rect)


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

            # Atualiza dinossauros
            for dino in ga.population:
                obstacle_distance = min([c.rect.left - dino.rect.right for c in cacti] or [float('inf')])
                if dino.decide_jump(obstacle_distance):
                    if dino.rect.bottom == int(0.98 * height):
                        dino.isJumping = True
                        if pygame.mixer.get_init() != None:
                            jump_sound.play()
                        dino.movement[1] = -1 * dino.jumpSpeed

                dino.update()

            # Atualiza obstáculos
            for c in cacti:
                c.movement[0] = -1 * gamespeed
                for dino in ga.population:
                    if pygame.sprite.collide_mask(dino, c):
                        dino.isDead = True
                        if pygame.mixer.get_init() != None:
                            die_sound.play()

            for p in pteras:
                p.movement[0] = -1 * gamespeed
                for dino in ga.population:
                    if pygame.sprite.collide_mask(dino, p):
                        dino.isDead = True
                        if pygame.mixer.get_init() != None:
                            die_sound.play()

            # Desenha e atualiza a tela
            screen.fill(background_col)
            new_ground.draw()
            clouds.draw(screen)
            scb.draw()
            highsc.update(high_score)
            if high_score != 0:
                highsc.draw()
            cacti.draw(screen)
            pteras.draw(screen)
            for dino in ga.population:
                dino.draw()

            pygame.display.update()
            clock.tick(FPS)

            # Verifica se o jogo terminou
            if all(dino.isDead for dino in ga.population):
                gameOver = True
                if any(dino.score > high_score for dino in ga.population):
                    high_score = max(dino.score for dino in ga.population)

            if counter % 700 == 699:
                new_ground.speed -= 1
                gamespeed += 1

            counter = (counter + 1)

        ga.evolve()  # Evolui a população

    pygame.quit()


def main_ga():
    ga = GeneticAlgorithm()
    gameplay_ga(ga)
    ga.save_best_weights()


if __name__ == "__main__":
    main_ga()
