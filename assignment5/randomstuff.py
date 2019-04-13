def calculate_net(inputs, weights):
	net = 0
	for i in range(IMAGE_SIZE):
		net += inputs[i]*weights[i]
	return net

def calculate_sigmoid(net):
	sigmoid = 0
	net = -net
	sigmoid = 1+math.exp(net)
	return 1/sigmoid
