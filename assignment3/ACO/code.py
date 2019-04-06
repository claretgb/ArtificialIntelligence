"""
	Source code created for DVA340 - Artificiell Intelligens.
	Code writer:
		- Clara Torre García-Barredo.
	Code created on April 2019.
"""

# Imports and time count.
import matplotlib.pyplot as plt
from copy import copy
import random
import math

# Constants used in the code and global variables.
NUMBER_OF_LOCATIONS = 52
# I repeat location 1 at the end of the file.
NUMBER_OF_ANTS = 70
PHEROMONES_INITIAL_VALUE = 10
locations = [] #type: list
tau = [] #type: list
D = [] #type: list
neta = [] #type: list
L = [] #type: list
alpha = 0.65
beta = 0.35
p = 0.15
distances_paths = [] #type: list
global_best_path = [] #type: list
global_best_distance = 40000

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


# Auxiliar methods (not main) to help comprehension and coding.

"""
	This method reads the file input with
	all the locations and their information and
	creates the objects from the class Location.
"""
def read_file():
	global NUMBER_OF_LOCATIONS, locations
	input_file = open("assignment3/ACO/berlin52.tsp", "r")
	for line in input_file:
		split_line = line.split(" ")
		locations.append(Location(int(split_line.pop(0)), float(split_line.pop(0)), float(split_line.pop(0))))

def initialize_pheromones():
	global tau
	row = [] #type: list
	for i in range(NUMBER_OF_LOCATIONS):
		for j in range(NUMBER_OF_LOCATIONS):
			if i == j:
				row.append(0)
			else:
				row.append(PHEROMONES_INITIAL_VALUE)
		tau.append(copy(row))
		row.clear()

def initialize_distances():
	global D, locations
	row = [] #type: list
	for i in range(NUMBER_OF_LOCATIONS):
		for j in range(NUMBER_OF_LOCATIONS):
			row.append(distance_points(i, j))
		D.append(copy(row))
		row.clear()

def initialize_heuristic():
	global neta, D
	row = [] #type: list
	for i in range(NUMBER_OF_LOCATIONS):
		for j in range(NUMBER_OF_LOCATIONS):
			if D[i][j] != 0.0:
				heuristic = 1/(D[i][j])
				row.append(heuristic)
			else:
				row.append(0.0)
		neta.append(copy(row))
		row.clear()

def initialize_ants():
	global L
	L = []
	for k in range(NUMBER_OF_ANTS):
		L.append([0, 0])

def build_solution():
	global L
	for i in range(1,NUMBER_OF_LOCATIONS):
		for k in range(NUMBER_OF_ANTS):
			L[k].insert(-1, transition_rule(k))

def transition_rule(k):
	global L
	transition_result = 0
	possible_s = [] #type: list
	location_r = L[k][-1]
	probabilities = [] #type: list
	sum = 0
	for loc in range(NUMBER_OF_LOCATIONS):
		if loc not in L[k]:
			possible_s.append(loc)
			sum += math.pow(tau[location_r][loc], alpha) * math.pow(neta[location_r][loc], beta)
	for loc_s in possible_s:
		top = math.pow(tau[location_r][loc_s], alpha) * math.pow(neta[location_r][loc_s], beta)
		division = top / sum
		probabilities.append([loc_s, division])
	# Roulette wheel.
	sum_prob = 0
	prob_roulette = [] #type: list
	for i in range(len(probabilities)):
		sum_prob += probabilities[i][1]
	for i in range(len(probabilities)):
		prob_roulette.append(probabilities[i][1]/sum_prob)
	random_selected = random.random()
	random_sum = 0
	for i in range(len(prob_roulette)):
		random_sum += prob_roulette[i]
		if random_sum > random_selected:
			transition_result = probabilities[i][0]
			break
	return transition_result

def distance_points(i, j):
	location_a = locations[i]
	location_b = locations[j]
	inside = math.pow((location_b.coordinate_x - location_a.coordinate_x), 2) + math.pow((location_b.coordinate_y - location_a.coordinate_y), 2)
	distance = math.sqrt(inside)
	return distance

def calculate_distance_paths():
	global L, distances_paths
	best_distance = 40000
	for k in range(NUMBER_OF_ANTS):
		distance = 0
		for i in range(len(L[k])-1):
			distance += distance_points(L[k][i], L[k][i+1])
			distances_paths.append(distance)
		if distance < best_distance:
			best_distance = distance
			best_path = L[k]
	return best_distance, best_path

def update_pheromones():
	global p, L, distances_paths
	for i in range(NUMBER_OF_LOCATIONS):
		for j in range(NUMBER_OF_LOCATIONS):
			sum = 0
			for k in range(NUMBER_OF_ANTS):
				if i in L[k] and j == L[k][L[k].index(i)+1]:
					sum += 1/distances_paths[k]
			tau[i][j] = (1-p)*tau[i][j] + sum


# Main function.

read_file()
initialize_pheromones()
initialize_distances()
initialize_heuristic()
best_distance = 40000
iterations = 0
while global_best_distance > 9000:
	initialize_ants()
	build_solution()
	best_distance, best_path = calculate_distance_paths()
	if best_distance < global_best_distance:
		global_best_distance = best_distance
		print(global_best_distance)
		global_best_path = best_path
	update_pheromones()
	iterations += 1
print(global_best_path, global_best_distance)