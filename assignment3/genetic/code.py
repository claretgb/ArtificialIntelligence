"""
	Source code created for DVA340 - Artificiell Intelligens.
	Code writer:
		- Clara Torre García-Barredo.
	Code created on April 2019.
"""

# Imports and time count.
from array import array
from copy import copy
from copy import deepcopy
import random
import math
import time
start = time.time()

# Constants used in the code and global variables.
NUMBER_OF_LOCATIONS = 52
POP_SIZE = 50
STOP_ITER_NUMBER = 1000
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
	input_file = open("assignment3/genetic/berlin52.tsp", "r")
	for line in input_file:
		split_line = line.split(" ")
		locations.append(Location(int(split_line.pop(0)), float(split_line.pop(0)), float(split_line.pop(0))))

def random_path_generator():
	global individuals
	path = [] #type: list
	for i in range(NUMBER_OF_LOCATIONS):
		path.append(i+1)
	random.shuffle(path)
	i = path.index(1)
	aux = path[0]
	path[0] = path[i]
	path[i] = aux
	individual = Individual(path)
	individuals.append(individual)

def calculate_distance(path):
	global locations
	distance = 0
	for i in range(NUMBER_OF_LOCATIONS):
		if i == NUMBER_OF_LOCATIONS-1:
			location_i = locations[i]
			location_j = locations[0]
		else:
			location_i = locations[i]
			location_j = locations[path.locations.index(i+2)]
		inside = math.pow((location_j.coordinate_x - location_i.coordinate_x), 2) + math.pow((location_j.coordinate_y - location_i.coordinate_y), 2)
		distance_i = math.sqrt(inside)
		distance += distance_i
	return distance

def parents_selection():
	index = 0
	smallest = 40000
	sec_smallest = 40000
	max_index = 0
	max2_index = 0
	for path in individuals:
		if path.distance < smallest:
			smallest = path.distance
			max_index = index
		elif path.distance < sec_smallest:
			sec_smallest = path.distance
			max2_index = index
		index += 1	
	return individuals[max_index], individuals[max2_index]

def find_worst_individuals():
	index = 0
	biggest = 0
	sec_biggest = 0
	min_index = 0
	min2_index = 0
	for path in individuals:
		if path.distance > biggest:
			biggest = path.distance
			min_index = index
		elif path.distance > sec_biggest:
			sec_biggest = path.distance
			min2_index = index
		index += 1	
	return min_index, min2_index

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

def generate_offspring(parent_i, parent_j):
	global individuals
	children = [] #type: list
	for l in range(0,POP_SIZE//4):
		aux = [] #type: list
		rand1 = random.randint(1,NUMBER_OF_LOCATIONS-2)
		rand2 = random.randint(rand1,NUMBER_OF_LOCATIONS-1)
		offspring_i = [] #type: list
		for i in range(rand1, rand2):
			aux.append(parent_i.locations[i])
		for i in range(NUMBER_OF_LOCATIONS):
			if parent_j.locations[i] not in aux:
				offspring_i.append(parent_j.locations[i])
		for i in range(rand1, rand2):
			offspring_i.insert(i, aux[i-rand1])
		offspring_j = [] #type: list
		aux = [] #type: list
		rand1 = random.randint(1,NUMBER_OF_LOCATIONS-2)
		rand2 = random.randint(rand1,NUMBER_OF_LOCATIONS-1)
		for i in range(rand1, rand2):
			aux.append(parent_i.locations[i])
		for i in range(NUMBER_OF_LOCATIONS):
			if parent_j.locations[i] not in aux:
				offspring_j.append(parent_j.locations[i])
		for i in range(rand1, rand2):
			offspring_j.insert(i, aux[i-rand1])
		index_worst, index_2worst = find_worst_individuals()
		individuals[index_worst] = Individual(offspring_i)
		individuals[index_2worst] = Individual(offspring_j)
		children.append(index_worst)
		children.append(index_2worst)
	return children

def mutate_population(children):
	global individuals
	rand1 = random.randint(1,NUMBER_OF_LOCATIONS-1)
	rand2 = random.randint(1,NUMBER_OF_LOCATIONS-1)
	rand3 = random.randint(1,len(children)-1)
	aux = individuals[children[rand3]].locations[rand1]
	individuals[children[rand3]].locations[rand1] = individuals[children[rand3]].locations[rand2]
	individuals[children[rand3]].locations[rand2] = aux

# Main function.

read_file()
best_distance_yet = 40000
# We initialize the population.
for i in range(POP_SIZE):
	random_path_generator()
counter = 0
while True:
	# We select the parents.
	parent_i, parent_j = parents_selection()
	children = generate_offspring(parent_i, parent_j)
	mutate_population(children)
	best = select_best_individual()
	if best.distance < best_distance_yet:
		print("Best distance:", best.distance)
		best_distance_yet = best.distance
	if best.distance < 9000:
		if counter >= STOP_ITER_NUMBER:
			break
		counter += 1

print("This is the solution:")
print(best.locations)

print("Execution time:")
end = time.time()
print(end - start)