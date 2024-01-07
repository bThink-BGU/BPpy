import random
import itertools
from math import prod
from bppy.utils.weighted_sampling import *
from uuid import uuid4

request = "request"
waitFor = "waitFor"
block = "block"
mustFinish = "mustFinish"
priority = "priority"
localReward = "localReward"

class sync(dict):
	def __init__(self, *, request=None, waitFor=None, block=None, mustFinish=None, priority=None, localReward=None, **kwargs):
		#'''TODO: warn if req/waitFor/block are not BEvent or choice'''
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
	def __init__(self, data, repeat=1, replace=True, sorted=False, 
				*args, **kwargs):
		if not isinstance(data, dict):
			raise TypeError("data must be a dict")
		if not replace and repeat > len(data):
			raise ValueError("repeat must be smaller than the number of choices")
		self.repeat = repeat
		self.replace = replace
		self.sorted = sorted
		super().__init__(data, **kwargs)
		self._id = uuid4()

	# returns iterable
	def options(self):
		dist = [self.keys(), self.values()]
		if self.replace and not self.sorted:
			pv, pp = [itertools.product(l,
			repeat=self.repeat) for l in dist]
			combined_probs = [prod(event_probs) for event_probs in pp]
		elif self.replace and self.sorted:
			pv, pp = [itertools.combinations_with_replacement(l,
			r=self.repeat) for l in dist]
		elif not self.replace and self.sorted:
			pv = itertools.combinations(dist[0], r=self.repeat)
			pv, combined_probs = zip(*[sequence_probability_nr_s(self, perm)
							 	for perm in pv])
		elif not self.replace and not self.sorted:
			pv, pp = [itertools.permutations(l,
			r=self.repeat) for l in dist]
		else:
			raise RuntimeError("Invalid combination of replace and sorted")
		if self.repeat == 1:
			return zip([v[0] for v in pv], combined_probs)
		return zip(pv, combined_probs)

	def sample(self):
		if self.replace:
			res = random.choices(list(self.keys()),
					self.values(), k=self.repeat)
			if self.repeat == 1:
				return res[0]
			if self.sorted:
				sort(res)
			return res
		else:
			res = weighted_sample_without_replacement(list(self.keys()),
					self.values(), k=self.repeat)
			if self.repeat == 1:
				return res[0]
			if self.sorted:
				res.sort()
			return res
	
	def __eq__(self, other):
		return isinstance(other, choice) and self._id == other._id
