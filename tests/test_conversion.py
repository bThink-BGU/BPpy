import unittest
from bppy import *
from bppy.analysis.bprogram_converter import BProgramConverter

class TestBProgram(unittest.TestCase):

	def test_prism_conversion(self):
		@b_thread
		def main():
			r = yield Choice({'a': 0.2, 'b': 0.3, 'c': 0.5})
			yield sync({request: BEvent(f'event_{r}')})

		def bp_gen():
			return bp.BProgram(bthreads=[main()],
							event_selection_strategy=bp.SimpleEventSelectionStrategy())

		ver = DFSBProgramVerifier(bp_gen)
		ok, counter_example = ver.verify()
		converter = BProgramConverter(bp_gen, [bp.BEvent('a'), bp.BEvent('b'), bp.BEvent('c')])
		output = converter.to_prism(None)
		assert output
