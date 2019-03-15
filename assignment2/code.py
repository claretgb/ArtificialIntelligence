from array import array
from copy import copy
from copy import deepcopy
"""
	Source code created for DVA340 - Artificiell Intelligens.
	Code writer:
		- Clara Torre García-Barredo.
	Code created on March 2019.
"""

import time
start = time.time()
number_of_cities = 49

"""
	I use this class to keep all the information
	about the different cities.
"""
class City:
	name = ""
	straight_distance = 0
	connections = []  # type: list

	def __init__(self, name, straight_distance):
		self.name = name
		self.straight_distance = straight_distance
		self.connections = []

	def addConection(self, connection, distance):
		self.connections.append([connection, distance])

"""
	I use this class to keep all the information
	about the path from Malaga to Valladolid.
"""
class Solution:
	solution = []  # type: list
	final_distance = 0

	def __init__(self, solution, final_distance):
		self.solution = solution
		self.final_distance = final_distance

	def add(self, city):
		self.solution.append(city)
	
	def update_final_distance(self, distance):
		self.final_distance += distance

"""
	This method reads the file input with
	all the cities and their information and
	creates the objects from the class City.
"""
def read_file():
	global number_of_cities
	input_file = open("assignment2/cities.txt", "r")
	cities = {}  # type: list
	for line in input_file:
		split_line = line.split(" ")
		city = copy(City(split_line.pop(0), int(split_line.pop(0))))
		while len(split_line) != 0:
			city.addConection(split_line.pop(0), int(split_line.pop(0)))
		cities[city.name] = city
	return cities

"""
	This method sorts an array of cities
	from maximum to minimum attending to 
	their straight line distance with
	Valladolid for the Greedy algorithm.
"""
def sort_max(array_connections, cities):
	aux = []  # type: list
	for i in range(len(array_connections)):
		aux.append(cities[array_connections[i][0]])
	for i in range(len(array_connections)):
		for j in range(len(array_connections)):
			if i < j:
				if (cities[aux[i].name].straight_distance) > (cities[aux[j].name].straight_distance):
					aux[i] = aux[i]
					aux[j] = aux[j]
				else:
					extra = aux[i]
					aux[i] = aux[j]
					aux[j] = extra
	return aux

"""
	This method sorts an array of cities
	from maximum to minimum attending to 
	their straight line distance with
	Valladolid for the A* algorithm.
"""
def sort_max_a_star(array_connections, cities):
	aux = []  # type: list
	for i in range(len(array_connections)):
		aux.append(array_connections[i])
	for i in range(len(array_connections)):
		for j in range(len(array_connections)):
			if i < j:
				if aux[i][1] > aux[j][1]:
					aux[i] = aux[i]
					aux[j] = aux[j]
				else:
					extra = aux[i]
					aux[i] = aux[j]
					aux[j] = extra
	return aux

"""
	This method updates the distance between
	cities that has already been walked in the
	A* algorithm.
"""
def update_distance(distance, new_city, old_city):
	for connection in cities[new_city.name].connections:
		if connection[0] == old_city:
			new_road = connection[1]
	distance += new_road
	return distance

"""
	This is the method used to solve 
	the problem with the Greedy Best
	First Search algorithm.
"""
def greedy_algorithm(cities):
	stack = []  # type: list
	solution = Solution([], 0)
	stack.append(cities['Malaga'])
	while len(stack) > 0:
		city = stack.pop(0)
		solution.add(city.name)
		if city.name == 'Valladolid':
			break
		if len(cities[city.name].connections) == 1:
			stack.insert(0,cities[cities[city.name].connections[0][0]])
		else:
			aux = sort_max(cities[city.name].connections, cities)
			for i in range(0, len(cities[city.name].connections)):
				stack.insert(0,aux[i])
		for connection in city.connections:
			if connection[0] == stack[0].name:
				solution.update_final_distance(connection[1])
	return solution


"""
	This is the method used to solve 
	the problem with the A* algorithm.
"""
def a_star(cities):
	stack = []  # type: list
	solution = Solution([], 0)
	stack.append(cities['Malaga'])
	distance = 0
	while len(stack) > 0:
		city = stack.pop(0)
		solution.add(city.name)
		if city.name == 'Valladolid':
			break
		for i in range(len(cities[city.name].connections)):
			acc = distance + cities[city.name].connections[i][1] + cities[cities[city.name].connections[i][0]].straight_distance
			cities[city.name].connections[i].pop()
			cities[city.name].connections[i].append(acc)
		if len(cities[city.name].connections) == 1:
			stack.insert(0,cities[cities[city.name].connections[0][0]])
		else:
			aux = sort_max_a_star(cities[city.name].connections, cities)
			for i in range(0, len(cities[city.name].connections)):
				stack.insert(0,cities[aux[i][0]])
		distance = update_distance(distance, stack[0], city.name)
	solution.update_final_distance(distance)
	return solution



# Main function.
cities = read_file()
print("This is the Greedy solution:")
greedy_solution = greedy_algorithm(cities)
print(greedy_solution.solution, greedy_solution.final_distance)
print("This is the A* solution:")
astar_solution = a_star(cities)
print(astar_solution.solution, astar_solution.final_distance)
print("Execution time:")
end = time.time()
print(end - start)