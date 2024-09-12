import random
import matplotlib.pyplot as plt
from typing import List, Tuple

class TRex:
    def __init__(self):
        self.y = 0
        self.velocity = 0
        self.fitness = 0
        self.genome = [random.uniform(0, 1) for _ in range(3)]

    def jump(self, obstacle_distance):
        if self.y == 0 and obstacle_distance < self.genome[0] and random.random() < self.genome[1]:
            self.velocity = self.genome[2] * 10
        
        self.y += self.velocity
        self.velocity -= 1
        
        if self.y < 0:
            self.y = 0
            self.velocity = 0

class Obstacle:
    def __init__(self, x):
        self.x = x
        self.width = 20
        self.height = 40

class Game:
    def __init__(self, population_size=3):
        self.population = [TRex() for _ in range(population_size)]
        self.obstacle = Obstacle(800)
        self.speed = 5
        self.score = 0

    def update(self):
        self.score += 1
        self.obstacle.x -= self.speed
        if self.obstacle.x < -self.obstacle.width:
            self.obstacle.x = 800

        for trex in self.population:
            trex.jump(self.obstacle.x)
            if self.check_collision(trex):
                trex.fitness = self.score

    def check_collision(self, trex):
        if (0 < self.obstacle.x < 50 and
            trex.y < self.obstacle.height):
            return True
        return False

    def all_dead(self):
        return all(trex.fitness > 0 for trex in self.population)

def selection(population: List[TRex]) -> List[TRex]:
    return sorted(population, key=lambda x: x.fitness, reverse=True)[:2]

def crossover(parent1: TRex, parent2: TRex) -> TRex:
    child = TRex()
    split = random.randint(0, len(parent1.genome))
    child.genome = parent1.genome[:split] + parent2.genome[split:]
    return child

def mutation(trex: TRex, mutation_rate: float = 0.1):
    for i in range(len(trex.genome)):
        if random.random() < mutation_rate:
            trex.genome[i] = random.uniform(0, 1)

def evolution(generations: int = 10) -> Tuple[List[int], List[List[int]]]:
    best_scores = []
    all_scores = []

    for gen in range(generations):
        game = Game()
        while not game.all_dead():
            game.update()

        scores = [trex.fitness for trex in game.population]
        all_scores.append(scores)
        best_scores.append(max(scores))

        selected = selection(game.population)
        game.population = [
            crossover(selected[0], selected[1]) for _ in range(len(game.population))
        ]
        for trex in game.population:
            mutation(trex)

    return best_scores, all_scores

def plot_results(best_scores: List[int], all_scores: List[List[int]]):
    generations = range(1, len(best_scores) + 1)
    
    plt.figure(figsize=(12, 6))
    plt.plot(generations, best_scores, label='Melhor pontuação', marker='o')
    
    for i in range(3):
        individual_scores = [scores[i] for scores in all_scores]
        plt.plot(generations, individual_scores, label=f'Indivíduo {i+1}', linestyle='--', marker='x')
    
    plt.xlabel('Geração')
    plt.ylabel('Pontuação')
    plt.title('Desempenho dos indivíduos ao longo das gerações')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    best_scores, all_scores = evolution(10)
    plot_results(best_scores, all_scores)
