import pygame as pg
import random
import os

# Classe base Obstacle (Obstáculo)
class Obstacle():
    def __init__(self, vel):
        # Inicializa a posição e a velocidade do obstáculo
        self.x = 830  # Posição inicial no eixo x (fora da tela à direita)
        self.vel = vel  # Velocidade do obstáculo
        self.path = os.getcwd() + '/' + 'imagens' + '/'  # Caminho das imagens dos obstáculos

    # Atualiza a posição do obstáculo
    def update(self):
        self.x -= self.vel  # Move o obstáculo para a esquerda com base na velocidade

    # Desenha o obstáculo na janela (função será implementada nas subclasses)
    def draw(self, window):
        pass

    # Desenha a hitbox do obstáculo para fins de debug
    def draw_hitbox(self, window):
        pg.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), 1)  # Desenha um retângulo em torno do obstáculo

    # Verifica se há colisão entre o dinossauro e o obstáculo
    def collide(self, dino):
        # Cria dois retângulos (um para o obstáculo e outro para o dinossauro) e verifica se colidem
        if pg.Rect(self.x, self.y, self.width, self.height).colliderect(pg.Rect(dino.x, dino.y, dino.width, dino.height)):
            return True  # Retorna True se houver colisão
        else:
            return False  # Retorna False se não houver colisão

# Classe Cactus (subclasse de Obstacle)
class Cactus(Obstacle):

    def __init__(self, vel):
        # Inicializa a classe Cactus chamando a classe base Obstacle
        super().__init__(vel)

        # Seção de Imagem
        # Carrega 16 imagens de cactos e escolhe uma aleatoriamente
        self.img = [pg.image.load(self.path + 'cactus_' + str(i) + '.png') for i in range(0, 16)]
        self.r = random.randrange(0, 16)  # Escolhe um cacto aleatoriamente
        self.curr_cactus = self.img[self.r]  # Define o cacto atual

        # Seção de Propriedades
        self.color = (231, 76, 60)  # Cor da hitbox (para depuração)
        # Redimensiona a largura e a altura da imagem para 2/3 do tamanho original
        self.width = int(self.curr_cactus.get_width() * 2/3)
        self.height = int(self.curr_cactus.get_height() * 2/3)
        self.y = 296 - self.height  # Define a posição no eixo y para o cacto "encostar" no chão

    # Desenha o cacto na janela
    def draw(self, window):
        # Desenha o cacto redimensionado na posição (x, y)
        window.blit(pg.transform.scale(self.curr_cactus, (self.width, self.height)), (self.x, self.y))

        # Desenha a hitbox do cacto (para depuração)
        self.draw_hitbox(window)

# Classe Ptera (subclasse de Obstacle)
class Ptera(Obstacle):

    def __init__(self, vel):
        # Inicializa a classe Ptera chamando a classe base Obstacle
        super().__init__(vel)

        # Seção de Imagem
        # Carrega as imagens das asas do Pterodáctilo em duas posições diferentes
        self.img = [pg.image.load(self.path + 'ptera_0.png'), pg.image.load(self.path + 'ptera_1.png')]
        self.frame = 0  # Contador de quadros para animar as asas

        # Seção de Propriedades
        # Define a posição vertical (y) aleatoriamente entre 90 e 220 pixels
        self.y = random.randrange(90, 220)
        self.color = (44, 62, 80)  # Cor da hitbox (para depuração)
        # Redimensiona a largura e a altura da imagem do pterodáctilo para 2/3 do tamanho original
        self.height = int(self.img[0].get_height() * 2/3)
        self.width = int(self.img[0].get_width() * 2/3)

    # Desenha o pterodáctilo na janela
    def draw(self, window):
        # Alterna entre as duas imagens para animar as asas
        if self.frame >= 16:  # Se o contador de quadros passar de 16, reinicia o contador
            self.frame = 0
        # Desenha o pterodáctilo com a imagem correspondente ao quadro atual
        window.blit(pg.transform.scale(self.img[self.frame // 8], (61, 53)), (self.x, self.y))
        self.frame += 1  # Incrementa o contador de quadros

        # Desenha a hitbox do pterodáctilo (para depuração)
        self.draw_hitbox(window)
