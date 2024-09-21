import numpy as np

class Dino_Brain():

    def __init__(self):
        # Uma camada de entrada, uma camada oculta e uma camada de saída
        self.n_x = 5  # Número de neurônios na camada de entrada
        self.n_h = 7  # Número de neurônios na camada oculta
        self.n_y = 3  # Número de neurônios na camada de saída

        # Inicializa aleatoriamente os pesos e os vieses (biases) da rede neural
        self.neural_wiring = {}  # Dicionário para armazenar a estrutura da rede neural
        self.neural_wiring['W1'] = np.random.randn(self.n_h, self.n_x) * 0.1  # Pesos da camada oculta
        self.neural_wiring['b1'] = np.random.randn(self.n_h, 1) * 0.1  # Bias da camada oculta
        self.neural_wiring['W2'] = np.random.randn(self.n_y, self.n_h) * 0.1  # Pesos da camada de saída
        self.neural_wiring['b2'] = np.random.randn(self.n_y, 1) * 0.1  # Bias da camada de saída

    # Função que processa as observações e decide uma ação
    def think_about_action(self, x):

        # Função de ativação ReLu (Retificação Linear Unitaria)
        def relu(z):
            return z * (z > 0)  # Mantém apenas valores positivos (ativações)

        # Alimenta as observações atuais na rede neural feedforward
        def feed_forward_nn(x):
            z1 = np.dot(self.neural_wiring['W1'], x) + self.neural_wiring['b1']  # Calcula a ativação da camada oculta
            a1 = relu(z1)  # Aplica a função de ativação ReLu na camada oculta
            z2 = np.dot(self.neural_wiring['W2'], a1) + self.neural_wiring['b2']  # Calcula a ativação da camada de saída
            a2 = relu(z2)  # Aplica a função de ativação ReLu na camada de saída
            return np.argmax(a2)  # Retorna o índice da ação com o maior valor (decisão da ação)

        # Garante que o array de entrada tenha o formato correto
        x = x.reshape(self.n_x, 1)

        # Calcula a ação com base nas observações processadas pela rede neural
        action = feed_forward_nn(x)
        return action  # Retorna a ação decidida
