import pygame as pg
import random
import os

# Classe base que define o ambiente do jogo
class Environment():

    # Método de inicialização do ambiente
    def __init__(self):
        # Define o caminho onde as imagens estão armazenadas
        self.path = os.getcwd() + '/' + 'imagens' + '/'

    # Método para atualizar a posição dos objetos no ambiente
    def update(self):
        # Move o objeto para a esquerda conforme a velocidade
        self.x -= self.vel

    # Método para desenhar o objeto na janela do jogo
    def draw(self, window):
        # Renderiza a imagem do objeto na janela na posição (x, y)
        window.blit(self.img, (self.x, self.y))


# Classe para as nuvens, herdada de Environment
class Cloud(Environment):

    # Inicialização das nuvens
    def __init__(self):
        super().__init__()  # Chama o método __init__ da classe pai (Environment)
        self.x = 830  # Posição inicial no eixo X (fora da tela)
        self.y = random.randrange(50, 180)  # Posição aleatória no eixo Y, entre 50 e 180
        self.vel = 3  # Velocidade de movimento da nuvem
        self.img = pg.image.load(self.path + 'cloud.png')  # Carrega a imagem da nuvem
        self.width = self.img.get_width()  # Obtém a largura da imagem da nuvem

# Classe para o chão, herdada de Environment
class Ground(Environment):

    # Inicialização do chão
    def __init__(self, x, vel):
        super().__init__()  # Chama o método __init__ da classe pai (Environment)
        self.x = x  # Posição inicial no eixo X
        self.y = 277  # Posição fixa no eixo Y para o chão
        self.vel = vel  # Velocidade de movimento do chão
        self.img = pg.image.load(self.path + 'ground.png')  # Carrega a imagem do chão
        self.width = self.img.get_width()  # Obtém a largura da imagem do chão
