import pygame as pg
from bibliotecas.Brain import Dino_Brain
import numpy as np
import os

class Dino():

    def __init__(self):
        # Caminho para as imagens do dinossauro
        self.path = os.getcwd() + '/' + 'imagens' + '/'

        # Seção de Imagens
        self.img_run = [pg.image.load(self.path + 'dino_run_0.png'),  # Imagem do dinossauro correndo (frame 1)
                        pg.image.load(self.path + 'dino_run_1.png')]  # Imagem do dinossauro correndo (frame 2)

        self.img_duck = [pg.image.load(self.path + 'dino_duck_0.png'),  # Imagem do dinossauro abaixado (frame 1)
                         pg.image.load(self.path + 'dino_duck_1.png')]  # Imagem do dinossauro abaixado (frame 2)

        self.frame_run = 0  # Contador para animar a corrida
        self.frame_duck = 0  # Contador para animar o abaixar

        self.color = (41, 128, 185)  # Cor da hitbox (retângulo ao redor do dinossauro)

        # Seção de Propriedades
        self.x = 50  # Posição x do dinossauro
        self.y = 237  # Posição y do dinossauro (altura)
        self.width = 59  # Largura do dinossauro
        self.height = 63  # Altura do dinossauro

        self.score = 0  # Pontuação do dinossauro
        self.fitness = 0  # Valor de fitness (para o algoritmo genético)

        # Inicializa o cérebro do dinossauro (rede neural)
        self.brain = Dino_Brain()

        # Variáveis para controlar o pulo
        self.jump_count_const = 8  # Valor constante de salto
        self.jump_count_running_variable = self.jump_count_const  # Contador do pulo em execução

        # Estados do dinossauro
        self.is_running = True  # Indica se o dinossauro está correndo
        self.is_ducking = False  # Indica se o dinossauro está abaixado
        self.is_jumping = False  # Indica se o dinossauro está pulando

    def sense_environment(self, obstacles, speed):
        # Função para o dinossauro "sentir" o ambiente (usado como entrada para a rede neural)
        
        observation_dict = {}  # Dicionário para armazenar as observações

        if len(obstacles) == 0:
            # Se não houver obstáculos
            observation_dict['distance_dino_obstcl_x'] = 1  # Distância fictícia para o obstáculo no eixo X
            observation_dict['obstcl_y'] = 1  # Posição fictícia para o obstáculo no eixo Y
        else:
            # Se houver obstáculos, calcula a distância e a posição
            observation_dict['distance_dino_obstcl_x'] = (-1 * self.x + obstacles[0].x) / 870  # Distância até o obstáculo normalizada
            observation_dict['obstcl_y'] = (obstacles[0].y) / 400  # Posição do obstáculo no eixo Y normalizada

        # Define as demais observações
        observation_dict['dino_y'] = self.y / 400  # Posição Y do dinossauro normalizada
        observation_dict['dino_y_vel'] = self.jump_count_running_variable / 30  # Velocidade do pulo normalizada

        observation_dict['game_speed'] = speed / 200  # Velocidade do jogo normalizada

        # Retorna o vetor de observação como uma matriz numpy
        observation = np.array([observation_dict['distance_dino_obstcl_x'],
                                observation_dict['obstcl_y'],
                                observation_dict['dino_y'],
                                observation_dict['dino_y_vel'],
                                observation_dict['game_speed']])

        return observation

    def update(self, action):
        # Atualiza o estado do dinossauro e a pontuação com base na ação selecionada
        
        # Correr
        if action == 0 and not self.is_jumping:
            self.score += 1  # Aumenta a pontuação quando o dinossauro está correndo
            self.y = 237  # Posição Y para a corrida
            self.width = 59  # Largura durante a corrida
            self.height = 63  # Altura durante a corrida

        # Abaixar
        if action == 1 and not self.is_jumping:
            self.score += 0.5  # Penaliza o abaixar permanente
            self.height = 40  # Altura ao abaixar
            self.width = 79  # Largura ao abaixar
            self.y = 260  # Posição Y ao abaixar

        # Pular
        if action == 2:
            self.is_jumping = True  # Define que o dinossauro está pulando

        if self.is_jumping:
            self.score += 0.05  # Penaliza o pulo permanente
            self.width = 59  # Largura durante o pulo
            self.height = 63  # Altura durante o pulo
            if self.jump_count_running_variable >= -self.jump_count_const:
                neg = 1
                if self.jump_count_running_variable < 0:
                    neg = -1
                self.y -= np.power(np.abs(self.jump_count_running_variable), 2) * 0.5 * neg  # Calcula a altura do pulo
                self.jump_count_running_variable -= 0.7  # Atualiza o contador do pulo
            else:
                self.is_jumping = False  # Finaliza o pulo
                self.jump_count_running_variable = self.jump_count_const  # Reseta o contador do pulo
                self.width = 59  # Reseta a largura
                self.height = 63  # Reseta a altura
                self.y = 237  # Reseta a posição Y

    def draw(self, window):
        # Desenha o dinossauro na janela do jogo
        
        def reset(self):
            self.is_running = False  # Reseta o estado de corrida
            self.is_ducking = False  # Reseta o estado de abaixar

        def draw_hitbox(window):
            pg.draw.rect(window, self.color,  # Desenha a hitbox ao redor do dinossauro
                         (self.x, self.y, self.width, self.height), 1)

        # Animação de pulo
        if self.y < 237 or self.is_jumping:
            window.blit(pg.transform.scale(self.img_run[0], (59, 63)), (self.x, self.y))  # Desenha o dinossauro pulando

        # Animação de abaixar
        if self.y == 260:
            if self.frame_duck >= 16:
                self.frame_duck = 0  # Reseta o contador da animação de abaixar
            window.blit(pg.transform.scale(self.img_duck[self.frame_duck // 8], (79, 40)), (self.x, self.y))  # Desenha o dinossauro abaixado
            self.frame_duck += 1  # Incrementa o frame da animação

        # Animação de correr
        if self.y == 237:
            if self.frame_run >= 16:
                self.frame_run = 0  # Reseta o contador da animação de corrida
            window.blit(pg.transform.scale(self.img_run[self.frame_run // 8], (59, 63)), (self.x, self.y))  # Desenha o dinossauro correndo
            self.frame_run += 1  # Incrementa o frame da animação

        # Desenha a hitbox do dinossauro
        draw_hitbox(window)

        reset(self)  # Reseta os estados do dinossauro
