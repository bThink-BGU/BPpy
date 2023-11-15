import random
from uuid import uuid4

request = "request"
waitFor = "waitFor"
block = "block"
mustFinish = "mustFinish"
priority = "priority"
localReward = "localReward"

class sync(dict):
    def __init__(self, *, request=None, waitFor=None, block=None, mustFinish=None, priority=None, localReward=None, **kwargs):
        if request is not None:
            self["request"] = request
        if waitFor is not None:
            self["waitFor"] = waitFor
        if block is not None:
            self["block"] = block
        if mustFinish is not None:
            self["mustFinish"] = mustFinish
        if priority is not None:
            self["priority"] = priority
        if localReward is not None:
            self["localReward"] = localReward
        super().__init__(kwargs)


class choice(dict):
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
