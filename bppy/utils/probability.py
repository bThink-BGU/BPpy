import random
from uuid import uuid4

class Choice(dict): #add unique id
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._id = uuid4()

	def options(self):
		return list(self.keys())

	def sample(self):
		return random.choices(list(self.keys()), self.values(), k=1)[0]
	
	def __eq__(self, other):
		return self._id == other._id
