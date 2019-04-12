"""
	Source code created for DVA340 - Artificiell Intelligens.
	Code writer:
		- Clara Torre García-Barredo.
	Code created on March 2019.
"""
from array import array
from copy import copy
from copy import deepcopy

NUMBER_OF_IMAGES = 42000
PERCENTAGE_TRAINING = 0.70
PERCENTAGE_VALIDATION = 0.80
PERCENTAGE_TESTING = 1.0


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
	This method reads the file input with all the images
	and creates objects of the class Image.
"""
def read_file():
	input_file = open("assignment5/assignment5_train.csv", "r")
	training_set = [] 
	validation_set = []
	testing_set = []
	line_index = 0
	for line in input_file:
		split_line = line.split(",")
		label = split_line.pop(0)
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

training_set, validation_set, testing_set = read_file()