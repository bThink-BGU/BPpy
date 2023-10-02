import random

class Choice:
	def __init__(self, weights):
		self.weights = weights

	def sample(self):
		return random.choices(list(self.weights.keys()), self.weights.values(), k=1)[0]
