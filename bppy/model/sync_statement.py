import random
from uuid import uuid4

request = "request"
waitFor = "waitFor"
block = "block"
mustFinish = "mustFinish"
priority = "priority"
localReward = "reward"
weight = "weight"

class BSync(dict):
    pass


class Choice(dict):
	"""
    A class to represent a discrete choice object.

	Keys correspond to the possible choices, and values correspond to the probability of each choice.
    """
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._id = uuid4()

	def options(self):
		return list(self.keys())

	def sample(self):
		return random.choices(list(self.keys()), self.values(), k=1)[0]
	
	def __eq__(self, other):
		return self._id == other._id