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
NUMBER_BLOCKS = 49
neurons = [] #type: list
division_size = 7 #7x7 = 49 groups of 4x4 matrixes of pixels.
filters = [] #type: list
blocks = [] #type: list
block_row_length = 4 #block has 16 pixels

# Hiperparameters.
NUMBER_OF_FILTERS = 20 #K
FILTER_SIZE = 3 #F
STRIDE = 1 #S
PADDING = 0 #P
POOL_SIZE = 2 #2x2 matrix


"""
	I use this class to keep all the information
	about the different images.
"""
class Image:
	label = 0
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
		break
	return training_set, validation_set, testing_set

def random_weight_generator():
	number_of_weights = int(FILTER_SIZE**2)
	weights = [] #type: list
	for i in range(number_of_weights):
		weights.append(random.choice([-1,1]))
	return weights


def relu(x):
	if x <= 0:
		x = 0
	return x
	
def convolutional_layer():
	for i in range(NUMBER_BLOCKS):
		blocks.append([])

	relu_results = [] #type: list
	for i in range(NUMBER_OF_FILTERS):
		relu_results.append([])

	z = 0
	for i in range(IMAGE_SIZE):
		pixel = training_set[0].pixels[i]
		if i%(NUMBER_BLOCKS*block_row_length) == 0:
			z += 1
		blocks[int((i-z*NUMBER_BLOCKS*block_row_length)/block_row_length)].append(pixel)

	for filter in filters:
		for block in blocks:
			difference_down = block_row_length - FILTER_SIZE
			while difference_down >= 0:
				difference_right = block_row_length - FILTER_SIZE
				counter = 0
				while difference_right >= 0:
					sum = 0
					for i in range(FILTER_SIZE):
						sum += filter[i]*block[i+counter]
					relu_result = relu(sum)
					relu_results[filters.index(filter)].append(relu_result)
					counter += 1
					difference_right -= STRIDE
				difference_down -= STRIDE
	return relu_results
	
def pooling_layer(relu_results):
	pooling_results = [] #type: list
	for i in range(NUMBER_OF_FILTERS):
		pooling_results.append([])
	for index,filter_matrix in enumerate(relu_results):
		for i in range(0,len(filter_matrix),POOL_SIZE**2):
			aux = filter_matrix[i:i+POOL_SIZE**2]
			pool_res = max(aux)
			pooling_results[index].append(pool_res)
	return pooling_results

def fully_connected_layer(output_number):
	
	return None

def softmax():
	return None

def generate_filters():
	global filters
	for i in range(NUMBER_OF_FILTERS):
		filters.append(random_weight_generator())




# Main function.	

training_set, validation_set, testing_set = read_file()
"""for i in range(NUMBER_NEURONS):
	for j in range():
"""
generate_filters()

relu_results = convolutional_layer()
pool_results = pooling_layer(relu_results)