# Intro genetic algorithm implementation in Python
# Goal is to maximize value of Y = w1x1 + w2x2 + w3x3 + w4x4 + w5x5 + w6x6 for inputs [x1, x2,..., x6] by modifying
# weights [w1,...,w6]

import numpy
from simple_ga import ga_functions as ga

# Inputs of the equation
equation_inputs = [4, 2, 3.5, 5, -11, -4.7]
# Number of weights we are looking to optimize
num_weights = 6

# define number of solutions per population
sol_per_pop = 8

# define population size
pop_size = (sol_per_pop, num_weights)

# Creating the initial population
new_population = numpy.random.uniform(low=-4.0, high=4.0, size=pop_size)


num_generations = 10

num_parents_mating = 4

initial_fitness = ga.cal_pop_fitness(equation_inputs, new_population)
initial_population = new_population.copy()

for generation in range(num_generations):
    # measuring the fitness of each chromosome in the population
    fitness = ga.cal_pop_fitness(equation_inputs, new_population)

    # selecting the best parents in the population for mating
    parents = ga.select_mating_pool(new_population, fitness, num_parents_mating)

    # generating the next generation using crossover
    offspring_crossover = ga.crossover(parents, offspring_size=(pop_size[0] - parents.shape[0], num_weights))

    # adding some variations to the offspring using mutation
    offspring_mutation = ga.mutation(offspring_crossover)

    # creating the new population based on the parents and offspring
    new_population[0:parents.shape[0], :] = parents
    new_population[parents.shape[0]:, :] = offspring_mutation

final_fitness = ga.cal_pop_fitness(equation_inputs, new_population)

print(f"\nInital population before GA:\n\t{initial_population}\n")
print(f"\nInital fitness before {num_generations} generations of mating:\n\t{initial_fitness}\n")
print(f"\nFinal fitness after {num_generations} generations of mating:\n\t{final_fitness}")
print(f"\nFinal population after GA:\n\t{new_population}")