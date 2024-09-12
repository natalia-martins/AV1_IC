import random
import numpy as np
from trex_runner import Game
from trex_runner.agents import NeuralAgent

# Função de seleção por Torneio
def torneio(populacao, fitness, tamanho_torneio=3):
    competidores = random.sample(list(zip(populacao, fitness)), tamanho_torneio)
    competidores.sort(key=lambda x: x[1], reverse=True)  # Ordena pelos melhores
    return competidores[0][0]  # Retorna o melhor agente

# Função de crossover entre dois pais
def crossover(pai1, pai2, taxa_cruzamento=0.5):
    filho1 = NeuralAgent()
    filho2 = NeuralAgent()
    
    for i in range(len(pai1.weights)):
        if random.random() < taxa_cruzamento:
            filho1.weights[i] = pai1.weights[i]
            filho2.weights[i] = pai2.weights[i]
        else:
            filho1.weights[i] = pai2.weights[i]
            filho2.weights[i] = pai1.weights[i]
    
    return filho1, filho2

# Função de mutação
def mutacao(agente, taxa_mutacao=0.1):
    for i in range(len(agente.weights)):
        if random.random() < taxa_mutacao:
            agente.weights[i] += np.random.normal(0, 0.1)  # Pequena mutação gaussiana
    return agente

# Função de avaliação da população
def avaliar_populacao(populacao, jogo):
    fitness = []
    for agente in populacao:
        agente.fitness = jogo.run(agent=agente)
        fitness.append(agente.fitness)
    return fitness

# Configurações
num_geracoes = 20
tamanho_populacao = 50
taxa_mutacao = 0.1
taxa_cruzamento = 0.5
tamanho_torneio = 3

# Inicializando o jogo e a população inicial
jogo = Game(visible=True)
populacao = [NeuralAgent() for _ in range(tamanho_populacao)]

# Algoritmo Evolutivo
for geracao in range(num_geracoes):
    print(f"Geracao {geracao+1}")
    
    # Avaliar a população
    fitness = avaliar_populacao(populacao, jogo)
    print(f"Melhor fitness da geração: {max(fitness)}")
    
    nova_populacao = []
    
    # Seleção, crossover e mutação para criar nova população
    while len(nova_populacao) < tamanho_populacao:
        pai1 = torneio(populacao, fitness, tamanho_torneio)
        pai2 = torneio(populacao, fitness, tamanho_torneio)
        
        filho1, filho2 = crossover(pai1, pai2, taxa_cruzamento)
        
        filho1 = mutacao(filho1, taxa_mutacao)
        filho2 = mutacao(filho2, taxa_mutacao)
        
        nova_populacao.extend([filho1, filho2])
    
    populacao = nova_populacao[:tamanho_populacao]  # Substituir pela nova geração

# Exibir os resultados finais
melhor_individuo = max(populacao, key=lambda agente: agente.fitness)
print(f"Melhor indivíduo tem fitness: {melhor_individuo.fitness}")
