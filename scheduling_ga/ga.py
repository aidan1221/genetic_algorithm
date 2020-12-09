from random import choice
from random import seed

def fitness_calc(population):

    population_w_fitness = []
    for sch in population:
        # overlap = total amount of overlapping time between speakers, 1 = 30 minutes (00:30)
        overlap = 0
        individuals = [sch[i:i + 11] for i in range(0,len(sch),11)]

        rooms_times = [{"room": x[4:7], "time":int(x[7:11], 2)} for x in individuals]

        for i in rooms_times:
            for j in rooms_times:
                if i["room"] != j["room"]:
                    time_overlap = abs(i["time"] - j["time"])
                    if time_overlap < 4:
                        overlap += 4 - time_overlap

        # add tuple of schedule + total overlap in schedule to returned population_w_fitness list
        population_w_fitness.append((sch, overlap))

    return population_w_fitness


def get_mating_parents(evaluated_population, num_population):

    pop_copy = evaluated_population.copy()

    top_parents = []

    for i in range(num_population // 2):

        fittest_parent = min(pop_copy, key=lambda x:x[1])
        top_parents.append(fittest_parent)
        pop_copy.remove(fittest_parent)

    return top_parents


def make_offspring(mating_parents, mutation_rate):

    children = []

    # crossover event
    # instead of picking a single point and swapping the entire schedule, I need to try picking individual speaker
    # timeslots and swapping them with other sections
    crossover_points = [x for x in range(0, len(mating_parents[0][0]), 11)]

    parent_pairs = [mating_parents[i:i + 2] for i in range(0, len(mating_parents), 2)]

    for parent_pair in parent_pairs:
        parent1, parent2 = parent_pair[0][0], parent_pair[1][0]
        child1, child2 = crossover(parent1, parent2, crossover_points)
        if (child1, child2) == (False, False):
            return False
        for child in child1, child2:
            children.append(child)

    # mutation event
    for i in range(len(children)):
        children[i] = mutate(children[i], mutation_rate)

    return children


def crossover(parent1, parent2, crossover_points):

    seed()

    # make children from crossover event
    count = 0
    while True:
        # avoid infinite loops
        count += 1
        if count > 10000:
            return False, False
        # make temp children from first randomly chosen crossover point
        cross_point = choice(crossover_points)
        child1_temp = parent1[:cross_point] + parent2[cross_point: cross_point + 11] + parent1[cross_point + 11:]
        child2_temp = parent2[:cross_point] + parent1[cross_point: cross_point + 11] + parent2[cross_point + 11:]


        # check children for conflicts
        conflict1 = has_conflicts(child1_temp)
        conflict2 = has_conflicts(child2_temp)

        if not conflict1 and not conflict2:
            break

    child1, child2 = child1_temp, child2_temp

    return child1, child2


def mutate(child, mutation_rate):

    seed()

    num_mutations = int(112 * mutation_rate)


    # only room and time bits should be mutatable so as not to create duplicate speakers - skip least significant bit to avoid
    valid_points = [4, 5, 6, 7, 8, 9, 10]
    mutation_points = [x + (11 * i) for x in valid_points for i in range(len(child) // 11)]
    least_significant_bits = [6, 10]
    for i in range(len(child)//11):
        for d in least_significant_bits:
            mutation_points.remove(d + (11 * i))
    mutation_points.sort()
    mutated_child = ""
    for i in range(num_mutations):
        while True:

            mut_point = choice(mutation_points)

            mutated_child = child[:mut_point] + str(int(not int(child[mut_point]))) + child[mut_point + 1:]

            if not has_conflicts(mutated_child):
                break

    return mutated_child


def has_conflicts(schedule):
    """
    Check a given schedule for direct conflicts within a given room

    :param schedule: binary string representing a proposed schedule
    :return: Boolean, True if schedule has conflicts, False otherwise
    """

    # overlap = total amount of overlapping time between speakers, 1 = 30 minutes (00:30)

    individuals = [schedule[i:i + 11] for i in range(0, len(schedule), 11)]

    speakers_rooms_times = [{"speaker": x[0:4], "room": x[4:7], "time": int(x[7:11], 2)} for x in individuals]

    for i in speakers_rooms_times:
        for j in speakers_rooms_times:
            if i["speaker"] != j["speaker"] and i["room"] == j["room"]:
                time_overlap = abs(i["time"] - j["time"])
                if time_overlap < 4:
                    return True

    return False


def get_fittest(pop_w_fitness):

    fittest_individual = min(pop_w_fitness, key=lambda x: x[1])

    return fittest_individual


def GA(population, num_generations, num_population, mutation_rate):

    pop_w_fitness = fitness_calc(population)
    initial_fittest = get_fittest(pop_w_fitness)

    for gen in range(num_generations):

        print(f"\nStart of generation {gen + 1}...", end="")

        mating_parents = get_mating_parents(pop_w_fitness, num_population)

        children = make_offspring(mating_parents, mutation_rate)

        if children is False:
            print("Infinite loop encountered")
            return False, False

        population = [x[0] for x in mating_parents] + children

        pop_w_fitness = fitness_calc(population)

        fittest_individual = get_fittest(pop_w_fitness)

        print(f"End of generation {gen + 1}...", end="")

    print(f"\nInitial fittest = {initial_fittest}\nFinal fittest = {fittest_individual}")
    return True, fittest_individual


def create_initial_population(num_population, speaker_genes, room_genes, time_genes):

    population = []

    for i in range(num_population):
        individual = []
        taken_room_times = []
        for j in list(speaker_genes.values()):
            speaker = j
            room = choice(list(room_genes.values()))
            time = choice(list(time_genes.values()))
            while room + time in taken_room_times:
                room = choice(list(room_genes.values()))
                time = choice(list(time_genes.values()))

            if int(time, 2) > 3:
                for k in range(-3, 4):
                    taken_time = str(bin(int(time, 2) + k))[2:].zfill(4)
                    taken_room_times.append(room + taken_time)
            else:
                start_index = -4 + (4 - int(time, 2))
                for k in range(start_index, 4):
                    taken_time = str(bin(int(time, 2) + k))[2:].zfill(4)
                    taken_room_times.append(room + taken_time)
            individual.append(speaker + room + time)

        population.append("".join(individual))

    return population

