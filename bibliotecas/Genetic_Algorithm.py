import numpy as np
from bibliotecas.Dino import *

# Passo 1: Criação da população inicial
def create_new_population(population_size):
    active_dinos = []
    all_dinos = []

    # Cria uma nova população de dinossauros
    for i in range(population_size):
        dino = Dino()
        active_dinos.append(dino)  # É importante que ambas as listas contenham os mesmos dinossauros
        all_dinos.append(dino)

    return all_dinos, active_dinos

# Passo 2: Seleção
def calculate_fitness(all_dinos):
    # Obtém as pontuações de todos os dinossauros e calcula, para cada dinossauro,
    # uma pontuação de fitness normalizada

    for dino in all_dinos:
        dino.score = dino.score**2  # Eleva a pontuação ao quadrado para aumentar a diferenciação

    sum = 0
    for dino in all_dinos:
        sum += dino.score  # Calcula a soma das pontuações

    for dino in all_dinos:
        dino.fitness = dino.score / sum  # Calcula o fitness como a fração da pontuação do dino em relação à soma total

    return all_dinos

# Cria o pool de acasalamento com base no fitness dos dinossauros
def create_mating_pool(all_dinos):
    # Quanto maior o fitness do dinossauro, mais vezes ele será representado
    # no pool de acasalamento. Portanto, será mais frequentemente selecionado
    # para reprodução (Passo 3)

    # A criação desse pool leva a uma divisão exponencial de fitness,
    # onde os dinossauros mais aptos são representados exponencialmente.

    mating_pool = []
    for dino in all_dinos:
        f = int(dino.fitness * len(all_dinos) * 10)  # O fitness determina quantas vezes o dinossauro é adicionado ao pool
        for i in range(f):
            mating_pool.append(dino)

    # Ordena o pool de acasalamento pelo fitness dos dinossauros. O mais apto será o primeiro
    mating_pool = sorted(mating_pool, key=lambda dino: dino.fitness)[::-1]

    # Seleção natural: apenas os 10% melhores sobrevivem e podem se reproduzir
    mating_pool = mating_pool[0:(len(mating_pool) // 10)]

    return mating_pool

# Passo 3: Reprodução
def create_next_generation(population_size, dino_mating_pool):

    all_dinos = []
    active_dinos = []

    # Função para realizar o crossover entre o DNA do pai e da mãe
    def crossover(father_DNA, mother_DNA):
        # Devido ao design da função create_mating_pool, o crossover torna-se
        # menos significativo com o tempo. No final, apenas clones de dinossauros
        # similares acasalam.

        crossover_DNA = {}

        heritage_percentage = np.random.randint(11) * 0.1  # Define a porcentagem de herança

        for index in father_DNA.keys():
            # Cria uma cópia profunda do DNA do pai, para que o crossover_DNA
            # tenha a mesma forma que a geração anterior
            crossover_DNA[index] = np.copy(father_DNA[index])

            orig_shape = father_DNA[index].shape
            for i in range(orig_shape[0]):
                for j in range(orig_shape[1]):
                    # Combina o DNA da mãe e do pai com base na porcentagem de herança
                    if np.random.random() < heritage_percentage:
                        crossover_DNA[index][i, j] = mother_DNA[index][i, j]

        return crossover_DNA

    # Função para mutar o DNA
    def mutate(DNA):

        # Função para mutar o genoma individualmente
        def mutate_genome(S):
            orig_shape = S.shape
            for i in range(orig_shape[0]):
                for j in range(orig_shape[1]):
                    # Aplica mutações ao genoma com base na taxa de mutação
                    if np.random.random() < mutation_rate:
                        S[i, j] = np.random.randn() * mutation_magnitude

            return S.reshape(orig_shape)

        mutation_rate = 0.05  # Define a taxa de mutação
        # Uma taxa de mutação mais alta leva a uma estagnação no início,
        # mas acelera o progresso a longo prazo. Uma taxa muito alta (> 0.09)
        # pode levar à estagnação.

        mutation_magnitude = 0.1  # Define a magnitude da mutação

        mutated_DNA = {}

        for i in DNA.keys():  # Aplica a mutação ao DNA
            mutated_DNA[i] = mutate_genome(np.copy(DNA[i]))

        return mutated_DNA

    # Criação de uma nova geração
    for i in range(population_size):

        # Seleciona aleatoriamente os parceiros de acasalamento
        a = np.random.randint(0, len(dino_mating_pool))
        b = np.random.randint(0, len(dino_mating_pool))

        # Crossover e mutação
        father_DNA = {}
        mother_DNA = {}

        # Copia o DNA neural (fiação neural) do pai e da mãe selecionados aleatoriamente
        for i in dino_mating_pool[0].brain.neural_wiring.keys():
            father_DNA[i] = np.copy(dino_mating_pool[a].brain.neural_wiring[i])
            mother_DNA[i] = np.copy(dino_mating_pool[b].brain.neural_wiring[i])

        crossover_DNA = crossover(father_DNA, mother_DNA)  # Realiza o crossover
        child_DNA = mutate(crossover_DNA)  # Aplica mutação ao DNA resultante

        # Cria um novo dinossauro
        child = Dino()

        # Herda o DNA resultante do crossover e mutação
        for i in child.brain.neural_wiring.keys():
            child.brain.neural_wiring[i] = child_DNA[i]

        all_dinos.append(child)  # Adiciona o novo dinossauro à lista de todos os dinossauros
        active_dinos.append(child)  # Adiciona o novo dinossauro à lista de dinossauros ativos

    return all_dinos, active_dinos  # Retorna a nova geração de dinossauros
