import random

# Exemplo simples de cromossomo
class DinoAgent:
    def __init__(self, genes):
        self.genes = genes  # Parâmetros evolutivos (pesos de uma rede neural, etc.)
        self.fitness = 0  # Valor da aptidão

    def play_game(self):
        # Aqui você conecta com a biblioteca chrome-trex-rush para jogar o jogo.
        # Use os genes para controlar o comportamento do dinossauro.
        self.fitness = self.evaluate_performance()

    def evaluate_performance(self):
        # Função de aptidão (exemplo usando distância)
        return random.randint(1, 1000)  # Exemplo de avaliação aleatória

# Algoritmo Genético básico
def genetic_algorithm():
    population = [DinoAgent([random.random() for _ in range(10)]) for _ in range(20)]

    for generation in range(100):  # Itera por 100 gerações
        for agent in population:
            agent.play_game()

        population.sort(key=lambda agent: agent.fitness, reverse=True)  # Ordena pela aptidão

        # Seleciona os melhores agentes
        parents = population[:10]
        children = []

        # Cruzamento e mutação
        for _ in range(10):
            parent1, parent2 = random.sample(parents, 2)
            child_genes = crossover(parent1.genes, parent2.genes)
            mutate(child_genes)
            children.append(DinoAgent(child_genes))

        # Cria a nova geração
        population = parents + children

# Funções de cruzamento e mutação
def crossover(genes1, genes2):
    return [(g1 + g2) / 2 for g1, g2 in zip(genes1, genes2)]

def mutate(genes, mutation_rate=0.01):
    for i in range(len(genes)):
        if random.random() < mutation_rate:
            genes[i] = random.random()

genetic_algorithm()
