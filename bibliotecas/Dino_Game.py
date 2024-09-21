import pygame as pg
import random
import os
import numpy as np
from sys import exit

from bibliotecas.Dino import *
from bibliotecas.Obstacles import *
from bibliotecas.Background import *

class DinoGame():

    def __init__(self):

        # Inicializa os parâmetros da tela
        pg.init()
        self.disp_x = 800  # Largura da tela
        self.disp_y = 350  # Altura da tela
        self.FPS = 60  # Frames por segundo
        pg.display.set_caption('Dino_game')  # Título da janela
        self.window = pg.display.set_mode((self.disp_x, self.disp_y))  # Cria a janela do jogo
        self.window_color = (247,247,247)  # Cor de fundo da janela (branco)
        self.clock = pg.time.Clock()  # Relógio do pygame para controlar o tempo

        self.game_score = 0  # Pontuação do jogo

        # Incrementadores do jogo
        self.cloud_counter = 60  # Contador de nuvens
        self.cloud_threshold = np.random.randint(60,100)  # Limite para adicionar uma nova nuvem
        self.obstacle_counter = 0  # Contador de obstáculos
        self.obstacle_threshold = np.random.randint(40,60)  # Limite para adicionar um novo obstáculo
        self.speed_counter = 0  # Contador de velocidade

        # Listas de objetos do jogo
        self.obstacles = []  # Lista de obstáculos (cactos, pterossauros, etc.)
        self.grounds = []  # Lista do chão
        self.clouds = []  # Lista de nuvens

        # Velocidade do jogo
        self.vel = 15  # Velocidade inicial do jogo

        self.add_obstacle()  # Adiciona o primeiro obstáculo

    def add_clouds(self):
        # Adiciona uma nova nuvem quando o contador atingir o limite
        if self.cloud_counter == self.cloud_threshold:
            self.clouds.append(Cloud())  # Adiciona uma nova nuvem à lista
            self.cloud_threshold = np.random.randint(70,120)  # Define um novo limite para adicionar outra nuvem
            self.cloud_counter = 0  # Reseta o contador de nuvens

    def add_ground(self):
        # Adiciona o chão ao jogo
        if len(self.grounds) == 0:
            # Adiciona duas partes do chão (uma após a outra)
            self.grounds.append(Ground(0, self.vel))
            self.grounds.append(Ground(self.disp_x, self.vel))

        if len(self.grounds) == 1:
            # Garante que sempre haja duas partes do chão
            self.grounds.append(Ground(self.disp_x, self.vel))

    def add_obstacle(self):
        # Adiciona um novo obstáculo quando o contador atingir o limite
        if self.obstacle_counter == self.obstacle_threshold:
            r = random.randrange(0, 4)  # Gera um número aleatório
            if r < 2:
                # Adiciona um cacto como obstáculo
                self.obstacles.append(Cactus(vel=self.vel))
            else:
                # Adiciona um pterossauro como obstáculo
                self.obstacles.append(Ptera(vel=self.vel))

            self.obstacle_counter = 0  # Reseta o contador de obstáculos
            self.obstacle_threshold = np.random.randint(40, 60)  # Define um novo limite para o próximo obstáculo

    def update_obstacles(self):
        # Atualiza os obstáculos existentes
        for i in self.obstacles:
            i.update()  # Atualiza a posição do obstáculo

            # Remove o obstáculo quando ele sai da tela
            if i.x < (i.width * -1):
                self.obstacles.pop(self.obstacles.index(i))  # Remove o obstáculo da lista
                self.reward = 1  # Recompensa ao passar por um obstáculo

    def update_clouds(self):
        # Atualiza as nuvens
        for i in self.clouds:
            i.update()  # Atualiza a posição da nuvem

            # Remove a nuvem quando ela sai da tela
            if i.x < (i.width * -1):
                self.clouds.pop(self.clouds.index(i))  # Remove a nuvem da lista

    def update_ground(self):
        # Atualiza o chão
        for i in self.grounds:
            i.update()  # Move o chão

            # Remove o chão quando ele sai da tela
            if i.x < (i.width * -1):
                self.grounds.pop(self.grounds.index(i))  # Remove o chão da lista

    def increment_counters(self):
        # Incrementa os contadores de velocidade, obstáculos e nuvens
        self.speed_counter += 1
        self.obstacle_counter += 1
        self.cloud_counter += 1

        # A cada 4 frames, incrementa a pontuação do jogo
        if self.speed_counter % 4 == 0:
            self.game_score += 1  # Aumenta a pontuação

    def increment_gamespeed(self):
        # Aumenta a velocidade do jogo a cada 1000 frames
        if self.speed_counter % 1000 == 0:
            self.vel += 2  # Aumenta a velocidade do jogo
            self.speed_counter = 0  # Reseta o contador de velocidade

    def step(self):
        # Função a ser implementada para avançar o jogo em um passo (pode ser usada para lógica do jogo)
        pass

    def render(self):
        # Função a ser implementada para renderizar o jogo na tela
        pass

    def close(self):
        # Fecha o jogo e o Pygame
        pg.display.quit()  # Fecha a janela do Pygame
        pg.quit()  # Encerra o Pygame
        print('Pontuação atual:', self.game_score)  # Exibe a pontuação final
        exit()  # Encerra o programa
