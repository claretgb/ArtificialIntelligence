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
NUMBER_NEURONS_OL = 10
LEARNING_RATE = 0.1 
neurons_hidden_layer = [] #type: list
neurons_output_layer = [] #type: list


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
	inputs = [] #type: list
	weights = [] #type: list
	output = 0

	def __init__(self, inputs, weights, output):
		self.inputs = inputs
		self.weights = weights
		net = self.calculate_net(inputs, weights)
		if output == 1:
			output = self.calculate_sigmoid(net)
		else:
			output = self.calculate_sign(net)
		self.output = output
	
	def calculate_net(self, inputs, weights):
		net = weights[0]
		for i in range(len(inputs)):
			net += inputs[i]*weights[i+1]
		return net

	def calculate_sigmoid(self, net):
		sigmoid = 0
		net = -net
		sigmoid = 1+math.exp(net)
		return 1/sigmoid

	def calculate_sign(self, net):
		if net > 0:
			sign = 1
		else:
			sign = -1
		return sign


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

def random_weight_generator(number_of_weights):
	weights = [] #type: list
	for i in range(number_of_weights):
		weights.append(random.uniform(-1,1))
	return weights

def learning_rule():
	return None

# Main function.

training_set, validation_set, testing_set = read_file()
for i in range(NUMBER_NEURONS_FHL):
	weights = random_weight_generator(IMAGE_SIZE+1)
	neurons_hidden_layer.append(Neuron(training_set[0].pixels, weights, 0))
for neuron in neurons_hidden_layer:
	print(neuron.output)
print()

inputs_output_layer = [] #type: list
for neuron in neurons_hidden_layer:
	inputs_output_layer.append(neuron.output)

for i in range(NUMBER_NEURONS_OL):
	weights = random_weight_generator(NUMBER_NEURONS_FHL+1)
	neurons_output_layer.append(Neuron(inputs_output_layer, weights, 1))
for neuron in neurons_output_layer:
	print(neuron.output)
print()

sum = 0.0
softmax_elem = [] #type: list
for neuron_output in neurons_output_layer:
	softmax_elem.append(math.exp(neuron_output.output))
	sum += math.exp(neuron_output.output)

for i in range(len(softmax_elem)):
	softmax_elem[i] = softmax_elem[i]/sum

output = softmax_elem.index(max(softmax_elem))
print("Output =", output)

# Creating target array.

t = [0,0,0,0,0,0,0,0,0,0] #type: list
t[training_set[0].label] = 1
print(t)

error_output = [] #type: list
for i in range(NUMBER_NEURONS_OL):
	error_output.append((t[i]-neurons_output_layer[i].output)*neurons_output_layer[i].output*(1-neurons_output_layer[i].output))
print(error_output)

for index,neuron in enumerate(neurons_output_layer):
	neuron.weights[0] = LEARNING_RATE*error_output[index]
	for i in range(NUMBER_NEURONS_FHL):
		neuron.weights[i] += LEARNING_RATE*error_output[index]*neuron.inputs[i]

error_hidden = [] #type: list
for i in range(NUMBER_NEURONS_FHL):
	sum = 0
	for j in range(NUMBER_NEURONS_OL):
		sum += error_output[j]*neurons_output_layer[j].weights[i+1]
	error_hidden.append((1-neurons_hidden_layer[i].output)*neurons_hidden_layer[i].output*sum)
print(error_hidden)

for index,neuron in enumerate(neurons_hidden_layer):
	neuron.weights[0] = LEARNING_RATE*error_hidden[index]
	for i in range(IMAGE_SIZE):
		aux = LEARNING_RATE*error_hidden[index]*neuron.inputs[i]
		neuron.weights[i] += aux
