import random

class Categorical:
	def __init__(self, pdf):
		self.pdf = pdf

	def sample(self):
		return random.choices(list(self.pdf.keys()), self.pdf.values(), k=1)[0]
