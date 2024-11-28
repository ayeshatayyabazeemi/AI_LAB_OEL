
import random as rndm
import time

# Part 1: Defining Genes and Chromosomes
def make_gene(initial=None):
    if initial is None:
        initial = [0] * 9
    mapp = {}
    gene = list(range(1, 10))
    rndm.shuffle(gene)
    for i in range(9):
        mapp[gene[i]] = i
    for i in range(9):
        if initial[i] != 0 and gene[i] != initial[i]:
            temp = gene[i], gene[mapp[initial[i]]]
            gene[mapp[initial[i]]], gene[i] = temp
            mapp[initial[i]], mapp[temp[0]] = i, mapp[initial[i]]
    return gene

def make_chromosome(initial=None):
    if initial is None:
        initial = [[0] * 9] * 9
    chromosome = []
    for i in range(9):
        chromosome.append(make_gene(initial[i]))
    return chromosome

# Part 2: Making First Generation
def make_population(count, initial=None):
    if initial is None:
        initial = [[0] * 9] * 9
    population = []
    for _ in range(count):
        population.append(make_chromosome(initial))
    return population

# Part 3: Fitness Function
def get_fitness(chromosome):
    """Calculate the fitness of a chromosome (puzzle)."""
    fitness = 0

    # Row fitness
    for row in chromosome:
        seen = {}
        for num in row:
            if num in seen:
                seen[num] += 1
            else:
                seen[num] = 1
        for key in seen:
            fitness -= (seen[key] - 1)

    # Column fitness
    for i in range(9):
        seen = {}
        for j in range(9):
            num = chromosome[j][i]
            if num in seen:
                seen[num] += 1
            else:
                seen[num] = 1
        for key in seen:
            fitness -= (seen[key] - 1)

    # Subgrid fitness
    for m in range(3):
        for n in range(3):
            seen = {}
            for i in range(3 * m, 3 * (m + 1)):
                for j in range(3 * n, 3 * (n + 1)):
                    num = chromosome[i][j]
                    if num in seen:
                        seen[num] += 1
                    else:
                        seen[num] = 1
            for key in seen:
                fitness -= (seen[key] - 1)

    return fitness



def pch(ch):
    for i in range(9):
        if i % 3 == 0 and i != 0:  # Print a horizontal line after every 3 rows
            print("---------------------")
        for j in range(9):
            if j % 3 == 0 and j != 0:  # Print a vertical line after every 3 columns
                print("|", end=" ")
            print(ch[i][j], end=" ")
        print("")  # Newline after each row


# Part 4: Crossover and Mutation
def crossover(ch1, ch2):
    new_child_1 = []
    new_child_2 = []
    for i in range(9):
        x = rndm.randint(0, 1)
        if x == 1:
            new_child_1.append(ch1[i])
            new_child_2.append(ch2[i])
        else:
            new_child_1.append(ch2[i])
            new_child_2.append(ch1[i])
    return new_child_1, new_child_2

def mutation(ch, pm, initial):
    for i in range(9):
        x = rndm.randint(0, 100)
        if x < pm * 100:
            ch[i] = make_gene(initial[i])
    return ch

# Part 5: Implementing The Genetic Algorithm
def read_puzzle(address):
    puzzle = []
    with open(address, 'r') as f:
        for row in f:
            temp = row.split()
            puzzle.append([int(c) for c in temp])
    return puzzle

def r_get_mating_pool(population):
    fitness_list = []
    pool = []
    for chromosome in population:
        fitness = get_fitness(chromosome)
        fitness_list.append((fitness, chromosome))
    fitness_list.sort()
    weight = list(range(1, len(fitness_list) + 1))
    for _ in range(len(population)):
        ch = rndm.choices(fitness_list, weight)[0]
        pool.append(ch[1])
    return pool

def get_offsprings(population, initial, pm, pc):
    new_pool = []
    i = 0
    while i < len(population):
        ch1 = population[i]
        ch2 = population[(i + 1) % len(population)]
        x = rndm.randint(0, 100)
        if x < pc * 100:
            ch1, ch2 = crossover(ch1, ch2)
        new_pool.append(mutation(ch1, pm, initial))
        new_pool.append(mutation(ch2, pm, initial))
        i += 2
    return new_pool

# Population size
POPULATION = 500  #2000

# Number of generations
REPETITION = 500   #1000

# Probability of mutation
PM = 0.1     #0.1

# Probability of crossover
PC = 0.7    #0.95

# Main genetic algorithm function

def genetic_algorithm(initial_file):
    initial = read_puzzle(initial_file)
    population = make_population(POPULATION, initial)
    generation=0
    for _ in range(REPETITION):
        generation+=1
        mating_pool = r_get_mating_pool(population)
        rndm.shuffle(mating_pool)
        population = get_offsprings(mating_pool, initial, PM, PC)
        fit = [get_fitness(c) for c in population]
        m = max(fit)
        print(f"Generation {generation}")
        if m == 0:
            return population
    return population


# Run the algorithm and time it
if __name__ == "__main__":
    tic = time.time()
    r = genetic_algorithm("puzzle_mild.txt")  # Adjust this path as necessary
    toc = time.time()
    print("time_taken: ", toc - tic)
    fit = [get_fitness(c) for c in r]
    m = max(fit)

    # Print the chromosome with the highest fitness
    for c in r:
        if get_fitness(c) == m:
            pch(c)
            break

