"""
	Source code created for DVA340 - Artificiell Intelligens.
	Code writer:
		- Clara Torre García-Barredo.
	Code created on April 2019.
"""
from array import array
from copy import copy
from copy import deepcopy
import random
import math

NUMBER_OF_IMAGES = 42000
IMAGE_SIZE = 784
PERCENTAGE_TRAINING = 0.70
PERCENTAGE_VALIDATION = 0.80
PERCENTAGE_TESTING = 1.0
LABEL_SOLVED = 0
NUMBER_NEURONS_FHL = 20
neurons = [] #type: list
division_size = 7 #7 groups of 4x4 matrixes of pixels.


"""
	I use this class to keep all the information
	about the different images.
"""
class Image:
	label = ""
	pixels = [] #type: list

	def __init__(self, label, pixels):
		self.label = label
		self.pixels = pixels

"""
	I use this class to keep all the information
	about the different neurons.
"""
class Neuron:
	output = 0

	def __init__(self, inputs, weights):
		net = self.calculate_net(inputs, weights)
		output = self.calculate_sigmoid(net)
		self.output = output
	
	def calculate_net(self, inputs, weights):
		net = weights[0]
		for i in range(IMAGE_SIZE):
			net += inputs[i]*weights[i+1]
		return net

	def calculate_sigmoid(self, net):
		sigmoid = 0
		net = -net
		sigmoid = 1+math.exp(net)
		return 1/sigmoid


"""
	This method reads the file input with all the images
	and creates objects of the class Image.
"""
def read_file():
	global NUMBER_OF_IMAGES, PERCENTAGE_TESTING, PERCENTAGE_TRAINING, PERCENTAGE_VALIDATION
	input_file = open("assignment5/assignment5_train.csv", "r")
	training_set = [] 
	validation_set = []
	testing_set = []
	line_index = 0
	for line in input_file:
		split_line = line.split(",")
		label = int(split_line.pop(0))
		pixels = [] #type: list
		while len(split_line) > 0:
			pixels.append(int(split_line.pop(0)))
		image = Image(label, pixels)
		if line_index < NUMBER_OF_IMAGES*PERCENTAGE_TRAINING:
			training_set.append(image)
		elif line_index < NUMBER_OF_IMAGES*PERCENTAGE_VALIDATION:
			validation_set.append(image)
		else:
			testing_set.append(image)
	return training_set, validation_set, testing_set

def random_weight_generator():
	global NUMBER_NEURONS_FHL
	weights = [] #type: list
	for i in range(IMAGE_SIZE+1):
		weights.append(random.uniform(-1.0,1.0))
	return weights






# Main function.	

training_set, validation_set, testing_set = read_file()
for i in range(NUMBER_NEURONS_FHL):
	neurons.append(Neuron(training_set[i].pixels,random_weight_generator()))