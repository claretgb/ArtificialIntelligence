"""
	Source code created for DVA340 - Artificiell Intelligens.
	Code writer:
		- Clara Torre García-Barredo.
	Code created on April 2019.
"""

# Imports and time count.
import matplotlib.pyplot as plt
import random
import math

# Constants used in the code and global variables.
NUMBER_OF_LOCATIONS = 52
POP_SIZE = 40
STOP_ITER_NUMBER = 1000
CHILD_NUMBER = POP_SIZE//2
locations = [] #type: list
individuals = [] #type: list

# Classes used to facilitate comprehension and coding.

"""
	I use this class to keep all the information
	about the different locations.
"""
class Location:
	name = 0
	coordinate_x = 0.0
	coordinate_y = 0.0

	def __init__(self, name, x, y):
		self.name = name
		self.coordinate_x = x
		self.coordinate_y = y

"""
	I use this class to keep all the information
	about the different individuals.
"""
class Individual:
	locations = [] #type: list
	distance = 0

	def __init__(self, locations):
		self.locations = locations
		self.distance = calculate_distance(self)


# Auxiliar methods (not main) to help comprehension and coding.

"""
	This method reads the file input with
	all the locations and their information and
	creates the objects from the class Location.
"""
def read_file():
	global NUMBER_OF_LOCATIONS, locations
	input_file = open("berlin52.tsp", "r")
	for line in input_file:
		split_line = line.split(" ")
		locations.append(Location(int(split_line.pop(0)), float(split_line.pop(0)), float(split_line.pop(0))))

"""
	This method generates random paths 
	to act as the initial population.
"""
def random_path_generator():
	global individuals
	path = [] #type: list
	for i in range(NUMBER_OF_LOCATIONS):
		path.append(i+1)
	random.shuffle(path)
	i = path.index(1)
	path[i] = path[0]
	path[0] = 1
	individual = Individual(path)
	individuals.append(individual)

"""
	This method calculates the total
	distance of a path, going through every
	location. It is my fitness function.
"""
def calculate_distance(path):
	global locations
	distance = 0
	for i in range(NUMBER_OF_LOCATIONS):
		location_i = locations[path.locations[i]-1]
		if i == NUMBER_OF_LOCATIONS-1:
			location_j = locations[0]
		else:
			location_j = locations[path.locations[i+1]-1]
		inside = math.pow((location_j.coordinate_x - location_i.coordinate_x), 2) + math.pow((location_j.coordinate_y - location_i.coordinate_y), 2)
		distance_i = math.sqrt(inside)
		distance += distance_i
	return distance

"""
	This is an auxiliary function
	in order to use the sort() method.
"""
def distance(element):
	return element.distance

"""
	This method finds the worst individuals 
	to kill them and replace them with the 
	generated offspring.
"""
def find_worst_individuals():
	aux = [] #type: list
	for i in individuals:
		aux.append(i)
	aux.sort(reverse = True, key = distance)
	for i in range(POP_SIZE - CHILD_NUMBER):
		aux.pop()
	return aux

"""
	This method finds the best individual 
	in the population to act as a parent.
"""
def select_best_individual():
	index = 0
	smallest = 40000
	max_index = 0
	for path in individuals:
		if path.distance > smallest:
			smallest = path.distance
			max_index = index
			index += 1
	return individuals[max_index]

"""
	This method generates the offspring
	using the best individual as a parent
	and another individual also as a parent.
"""
def generate_offspring(parent_i):
	global individuals
	children = [] #type: list
	for l in range(0,CHILD_NUMBER):
		aux = [] #type: list
		rand1 = random.randint(1,NUMBER_OF_LOCATIONS-2)
		rand2 = random.randint(rand1,NUMBER_OF_LOCATIONS-1)
		parent_j = parent_i
		while parent_j == parent_i:
			parent_j = individuals[random.randint(0, POP_SIZE-1)]
		if random.random() < 0.5:
			aux_par = parent_i
			parent_i = parent_j
			parent_j = aux_par
		offspring_i = [] #type: list
		for i in range(rand1, rand2):
			aux.append(parent_i.locations[i])
		for i in range(NUMBER_OF_LOCATIONS):
			if parent_j.locations[i] not in aux:
				offspring_i.append(parent_j.locations[i])
		for i in range(rand1, rand2):
			offspring_i.insert(i, aux[i-rand1])
		offspring = Individual(offspring_i)
		children.append(offspring)
	worst_indiv = find_worst_individuals()
	for i in range(len(children)):
		individuals[individuals.index(worst_indiv[i])] = children[i]
	return children

"""
	This method mutates a random number
	of children to avoid prematurity and 
	increase diversity.
"""
def mutate_population(children):
	global individuals
	mutated = [] #type: list
	rand3 = random.randint(1,len(children))
	for j in range(rand3, len(children)):
		if children[j] not in mutated:
			for k in range(0,1):
				rand1 = random.randint(1,NUMBER_OF_LOCATIONS-2)
				rand2 = random.randint(rand1,NUMBER_OF_LOCATIONS-1)
				difference = rand2 - rand1
				for i in range(difference):
					aux = children[j].locations[rand1+i]
					children[j].locations[rand1+i] = children[j].locations[rand2-i]
					children[j].locations[rand2-i] = aux

# Main function.

read_file()
best_distance_yet = 40000
# We initialize the population.
for i in range(POP_SIZE):
	random_path_generator()
distances = [] #type: list
generations = 0
grapth_gens = [] #type: list
while True:
	# We select the parents.
	parent_i = select_best_individual()
	children = generate_offspring(parent_i)
	mutate_population(children)
	best = select_best_individual()
	if best.distance < best_distance_yet:
		print("Best distance:", best.distance, "Generation:", generations)
		best_distance_yet = best.distance
		distances.append(best_distance_yet)
		grapth_gens.append(generations)
		counter = 0
	if best.distance < 9000:
		if counter >= STOP_ITER_NUMBER:
			break
		counter += 1
	generations += 1


plt.plot(grapth_gens, distances)
plt.xlabel('Generations')
plt.ylabel('Distances')
plt.show()
print("This is the solution:")
print(best.locations)