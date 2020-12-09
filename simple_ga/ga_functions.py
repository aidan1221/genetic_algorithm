import numpy


def cal_pop_fitness(equation_inputs, pop):
    # calculating the fitness value of each solution in the current population
    # the fitness function calculates the sum of products between each input and its corresponding weight
    fitness = numpy.sum(pop * equation_inputs, axis=1)
    return fitness


def select_mating_pool(pop, fitness, num_parents):
    # selecting the best individuals in the current generation as parents for producing the offspring of the next
    # generation

    parents = numpy.empty((num_parents, pop.shape[1]))
    for parent_num in range(num_parents):
        max_fitness_idx = numpy.where(fitness == numpy.max(fitness))
        max_fitness_idx = max_fitness_idx[0][0]
        parents[parent_num, :] = pop[max_fitness_idx, :]
        fitness[max_fitness_idx] = -99999999999

    return parents


def crossover(parents, offspring_size):
    offspring = numpy.empty(offspring_size)
    # the point at which crossover takes place between two parents
    # usually, it is at the center
    crossover_point = numpy.uint8(offspring_size[1]/2)

    for k in range(offspring_size[0]):
        # index of the first parent to mate
        parent1_idx = k % parents.shape[0]

        # index of second parent to mate
        parent2_idx = (k + 1) % parents.shape[0]

        # the new offspring will have the first half of its genes taken from the first parent
        offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]

        # the new offspring will have the second half of its genes taken from parent 2
        offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]

        return offspring


def mutation(offspring_crossover):
    # mutation changes a single gene in each offspring randomly
    for i in range(offspring_crossover.shape[0]):
        # the random value to be added to the gene
        random_val = numpy.random.uniform(-1.0, 1.0, 1)
        offspring_crossover[i, 4] = offspring_crossover[i, 4] + random_val

    return offspring_crossover


