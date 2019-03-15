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
	father = None
	distance_walked = 0
	a_star_value = 0

	def __init__(self, name, straight_distance):
		self.name = name
		self.straight_distance = straight_distance
		self.connections = []
		self.path_already_taken = []
		self.distance_walked = 0
		self.a_star_value = 0

	def addConection(self, connection, distance):
		self.connections.append([connection, distance])
	
	def change_father(self, city):
		self.father = city

	def update_distance_walked(self, distance):
		self.distance_walked = self.father.distance_walked + distance

	def update_astar(self):
		self.a_star_value = self.distance_walked + self.straight_distance

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
	cities = {} 
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
def sort_max(stack):
	for i in range(len(stack)):
		for j in range(len(stack)):
			if stack[i].straight_distance < stack[j].straight_distance:
				extra = stack[i]
				stack[i] = stack[j]
				stack[j] = extra
	return stack

"""
	This method sorts an array of cities
	from maximum to minimum attending to 
	their straight line distance with
	Valladolid for the A* algorithm.
"""
def sort_max_a_star(stack):
	for i in range(len(stack)):
		for j in range(i+1,len(stack)):
			if stack[i].a_star_value > stack[j].a_star_value:
				extra = stack[i]
				stack[i] = stack[j]
				stack[j] = extra
	return stack

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
		for i in range(0, len(cities[city.name].connections)):
			stack.append(cities[cities[city.name].connections[i][0]])
		stack = sort_max(stack)
		for connection in city.connections:
			if connection[0] == stack[0].name:
				solution.update_final_distance(connection[1])
	return solution


"""
	This is the method used to solve 
	the problem with the A* algorithm.
"""
def a_star(cities):
	stack = []  #type: list
	visited = [] #type: list
	solution = Solution([], 0)
	stack.append(cities['Malaga'])
	finished = False
	while len(stack) > 0:
		city_visited = True
		while city_visited:
			city = stack.pop(0)
			if city not in visited:
				city_visited = False
		visited.append(city)
		if city.name == 'Valladolid':
			break
		for i in range(len(cities[city.name].connections)):
			if cities[city.connections[i][0]].father is None and city.connections[i][0] != 'Malaga':
				cities[city.connections[i][0]].change_father(city)
				cities[city.connections[i][0]].update_distance_walked(city.connections[i][1])
				cities[city.connections[i][0]].update_astar()
		for i in range(0, len(city.connections)):
			stack.append(cities[city.connections[i][0]])
		stack = sort_max_a_star(stack)
	city_visited = city
	while not finished:
		solution.solution.insert(0,city_visited.name)
		city_visited = city_visited.father
		if city_visited == None:
			finished = True
	solution.update_final_distance(city.distance_walked)
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