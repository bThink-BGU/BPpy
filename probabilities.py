import random

class Choice(dict): #add unique id
	def options(self):
		return list(self.keys())

	def sample(self):
		return random.choices(list(self.keys()), self.values(), k=1)[0]
