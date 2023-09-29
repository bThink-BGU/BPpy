import random

class Categorical:
	def __init__(self, name, dist):
		self.name = name
		self.dist = dist

	def sample(self):
		return random.choices(list(self.dist.keys()), self.dist.values(), k=1)[0]
