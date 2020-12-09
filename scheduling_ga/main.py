from random import choice
import random
import scheduling_ga.ga as ga

# lecture scheduling simple GA implementation

random.seed()

# provide an even number for initial population TODO: convert to user input()
num_population = 36

num_generations = 100

mutation_rate = 0.8

rooms = ["Elm", "Pine", "Ash", "Oak", "Alder", "Maple", "Willow", "Cedar"]
speakers = []
for i in range(16):
    speakers.append(f"speaker{i}")

times = []
time = "8:00"
while time != "4:00":
    times.append(time)
    if time != "12:30":
        if time.split(":")[1] == "00":
            time = time.split(":")[0] + ":30"
        else:
            time = str(int(time.split(":")[0]) + 1) + ":00"
    else:
        time = "1:00"

room_genes = dict()
for i in range(len(rooms)):
    room_genes[rooms[i]] = str(bin(i))[2:].zfill(3)

speaker_genes = dict()
for i in range(len(speakers)):
    speaker_genes[speakers[i]] = str(bin(i))[2:].zfill(4)
time_genes = dict()
for i in range(len(times)):
    time_genes[times[i]] = str(bin(i))[2:].zfill(4)

print(room_genes)
print(speaker_genes)
print(time_genes)

# An organism is the combination <speaker_gene + room_gene + time_gene> for all 12 speakers
# Each speaker requires 2 hours to speak
# Randomly generate room + time assignments for each speaker, ensuring no direct conflicts in the same room

population = ga.create_initial_population(num_population, speaker_genes, room_genes, time_genes)

print([ga.has_conflicts(x) for x in population])

ga_success = ga.GA(population, num_generations, num_population, mutation_rate)
while not ga_success[0]:
    population = ga.create_initial_population(num_population, speaker_genes, room_genes, time_genes)
    ga_success = ga.GA(population, num_generations, num_population, mutation_rate)

print("\n")

fittest_individual = ga_success[1][0]
speakers = [fittest_individual[i:i+11] for i in range(0,len(fittest_individual), 11)]
assignments = []
mapping= []
for s in speakers:
    speaker = list(speaker_genes.keys())[list(speaker_genes.values()).index(s[:4])]
    room = list(room_genes.keys())[list(room_genes.values()).index(s[4:7])]
    time = list(time_genes.keys())[list(time_genes.values()).index(s[7:11])]
    time_int = int(s[7:11], 2)
    assignments.append({"speaker": speaker, "room": room, "time": time})
    mapping.append({"speaker": speaker, "room": room, "time": time_int})

illustration = dict()
for room in rooms:
    illustration[room] = []
    for item in mapping:
        if item["room"] == room:
            illustration[room].append(item["time"])
    illustration[room].sort()

print(assignments)
for room_key in illustration.keys():
    illustration_string = ""
    for i in range(len(illustration[room_key])):
        if i == 0:
            illustration_string += ("_ " * illustration[room_key][i]) + ("* " * 4)
        else:
            illustration_string += ("_ " * (illustration[room_key][i] - (illustration[room_key][i - 1] + 4))) + ("* " * 4)

    len_string = len(illustration_string)
    while not len(illustration_string) == 38:
        illustration_string += "_ "
    room_name = "{0: >7}".format(room_key)
    print(room_name + " : " + illustration_string)


# print(assignments)

