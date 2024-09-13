import numpy as np
from chrome_trex import DinoAgent, Game

import chrome_trex
print(dir(chrome_trex))



# Parâmetros do algoritmo genético
POPULATION_SIZE = 50
GENERATIONS = 100
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.7

# Função de seleção por torneio
def tournament_selection(population, fitness, tournament_size=5):
    selected = []
    for _ in range(len(population)):
        tournament = np.random.choice(len(population), tournament_size)
        best = tournament[0]
        for i in tournament:
            if fitness[i] > fitness[best]:
                best = i
        selected.append(population[best])
    return selected

# Função de crossover (cruzamento de dois indivíduos)
def crossover(parent1, parent2):
    if np.random.rand() < CROSSOVER_RATE:
        point = np.random.randint(0, len(parent1))
        child1 = np.concatenate((parent1[:point], parent2[point:]))
        child2 = np.concatenate((parent2[:point], parent1[point:]))
        return child1, child2
    return parent1, parent2

# Função de mutação
def mutate(individual):
    for i in range(len(individual)):
        if np.random.rand() < MUTATION_RATE:
            individual[i] += np.random.randn() * 0.1  # Perturbação pequena nos pesos
    return individual

# Função para salvar os pesos do melhor indivíduo
def save_best_individual(best_individual, generation):
    np.save(f'best_individual_gen_{generation}.npy', best_individual)

# Inicialização da população
def initialize_population(size):
    return [np.random.randn(10) for _ in range(size)]  # Supomos que o agente tem 10 genes/pesos

# Função de aptidão (fitness) para avaliar o desempenho dos dinossauros
def fitness_function(agent):
    game = Game()
    agent.run(game)  # Execute o agente no jogo
    return game.get_score()  # O fitness é baseado na pontuação alcançada

# Treinamento usando Algoritmos Genéticos
def genetic_algorithm():
    # Inicializando a população
    population = initialize_population(POPULATION_SIZE)
    fitness_history = []

    for generation in range(GENERATIONS):
        print(f'Iniciando geração {generation}')
        fitness = []

        # Avaliando o fitness de cada indivíduo
        for individual in population:
            agent = DinoAgent(individual)
            fit = fitness_function(agent)
            fitness.append(fit)

        fitness_history.append(np.max(fitness))

        # Exibindo progresso
        if generation == 0:
            print(f'Fitness inicial: {np.max(fitness)}')
        elif generation == GENERATIONS // 2:
            print(f'Fitness no meio do treinamento: {np.max(fitness)}')
        elif generation == GENERATIONS - 1:
            print(f'Melhor fitness na última geração: {np.max(fitness)}')

        # Seleção
        population = tournament_selection(population, fitness)

        # Cruzamento
        next_population = []
        for i in range(0, len(population), 2):
            parent1 = population[i]
            parent2 = population[(i+1) % len(population)]
            child1, child2 = crossover(parent1, parent2)
            next_population.extend([child1, child2])

        # Mutação
        population = [mutate(ind) for ind in next_population]

        # Salvar o melhor indivíduo
        best_individual = population[np.argmax(fitness)]
        save_best_individual(best_individual, generation)

    # Retorna o melhor agente
    return best_individual

if __name__ == "__main__":
    best_individual = genetic_algorithm()
    print(f'Treinamento concluído. Melhor agente salvo com os pesos: {best_individual}')
